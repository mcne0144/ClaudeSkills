// The agent loop: streams a turn from Claude, runs the knowledge tools in the
// browser, lets Anthropic run web search/fetch server-side, and repeats until
// the turn ends. History is append-only so thinking blocks replay unchanged.

import Anthropic from "@anthropic-ai/sdk";
import { AGENT_BRIEF, catalog, coreText, readSection, search } from "./knowledge";
import type { ApiMessage, Settings } from "./store";

type BetaTool = Anthropic.Beta.Messages.BetaToolUnion;
type BetaMessage = Anthropic.Beta.Messages.BetaMessage;
type ToolResult = Anthropic.Beta.Messages.BetaToolResultBlockParam;

// Built once per page load and never changed, so the prompt cache hits.
const SYSTEM_TEXT = `${AGENT_BRIEF}

# Knowledge base

You have a knowledge base written for you. Three core files are embedded below in full. Every other section is listed in the catalog: call search_knowledge to find sections by topic, then read_knowledge with a section id to read one in full. Prefer the knowledge base over memory for frameworks, history, vocabulary, the Jason Swet study and his reference network; use web search for anything current or not covered.

## Catalog

${catalog()}

## Core files

${coreText()}`;

const KNOWLEDGE_TOOLS: BetaTool[] = [
  {
    name: "search_knowledge",
    description:
      "Search Atelier's art direction knowledge base (art history atlas, design and typography history, visual vocabulary, advertising science and buyer psychology, buyer journeys and social algorithms, AI production tools, video/web/motion craft, brand building, the Jason Swet study and his reference network, methods and templates). Returns the best-matching sections with ids and snippets. Use before answering from memory on any of those topics.",
    eager_input_streaming: true,
    input_schema: {
      type: "object",
      properties: {
        query: { type: "string", description: "Keywords or a natural-language question" },
        max_results: { type: "integer", description: "1 to 10, default 6" },
      },
      required: ["query"],
    },
  },
  {
    name: "read_knowledge",
    description: "Read one knowledge base section in full by its id (from the catalog or search_knowledge results), e.g. '03-art-history-atlas#12'.",
    eager_input_streaming: true,
    input_schema: {
      type: "object",
      properties: { id: { type: "string" } },
      required: ["id"],
    },
  },
];

const WEB_TOOLS: BetaTool[] = [
  { type: "web_search_20260209", name: "web_search", max_uses: 8 },
  { type: "web_fetch_20260209", name: "web_fetch", max_uses: 6 },
];

export interface TurnCallbacks {
  onText(delta: string): void;
  onThinking(delta: string): void;
  onTool(label: string): void;
  onSource(source: { title: string; url: string }): void;
  onNotice(text: string): void;
}

function runLocalTool(name: string, input: unknown): { content: string; isError: boolean } {
  const args = (input && typeof input === "object" ? input : {}) as Record<string, unknown>;
  if (name === "search_knowledge") {
    if (typeof args.query !== "string" || !args.query.trim()) return { content: "query must be a non-empty string", isError: true };
    const n = typeof args.max_results === "number" ? Math.min(10, Math.max(1, Math.round(args.max_results))) : 6;
    const hits = search(args.query, n);
    return { content: hits.length ? JSON.stringify(hits, null, 1) : "No matching sections. Try other keywords or use web search.", isError: false };
  }
  if (name === "read_knowledge") {
    if (typeof args.id !== "string") return { content: "id must be a string", isError: true };
    const text = readSection(args.id);
    return text ? { content: text, isError: false } : { content: `No section with id ${args.id}`, isError: true };
  }
  return { content: `Unknown tool ${name}`, isError: true };
}

function describeServerTool(block: Anthropic.Beta.Messages.BetaServerToolUseBlock): string {
  const input = block.input as Record<string, unknown>;
  if (block.name === "web_search") return `Searched the web: ${String(input.query ?? "")}`;
  if (block.name === "web_fetch") return `Read ${String(input.url ?? "a page")}`;
  return `Used ${block.name}`;
}

/**
 * Runs one user turn to completion. `messages` must already end with the new
 * user message; assistant turns and tool results are appended in place.
 */
export async function runTurn(
  settings: Settings,
  messages: ApiMessage[],
  cb: TurnCallbacks,
  signal: AbortSignal,
): Promise<{ usage: string }> {
  const client = new Anthropic({ apiKey: settings.apiKey, dangerouslyAllowBrowser: true });
  const tools = settings.webSearch ? [...KNOWLEDGE_TOOLS, ...WEB_TOOLS] : KNOWLEDGE_TOOLS;
  let input = 0;
  let output = 0;
  let cached = 0;
  let jsonRetries = 0;

  for (let step = 0; step < 24; step++) {
    const stream = client.beta.messages.stream(
      {
        model: settings.model,
        max_tokens: 64000,
        betas: ["server-side-fallback-2026-07-01"],
        fallbacks: "default",
        thinking: { type: "adaptive", display: "summarized" },
        output_config: { effort: settings.effort },
        system: [{ type: "text", text: SYSTEM_TEXT, cache_control: { type: "ephemeral" } }],
        cache_control: { type: "ephemeral" },
        tools,
        messages,
      },
      { signal },
    );
    stream.on("text", (d) => cb.onText(d));
    stream.on("thinking", (d) => cb.onThinking(d));
    stream.on("contentBlock", (block) => {
      if (block.type === "server_tool_use") cb.onTool(describeServerTool(block));
      if (block.type === "web_search_tool_result" && Array.isArray(block.content)) {
        for (const r of block.content) if (r.type === "web_search_result") cb.onSource({ title: r.title, url: r.url });
      }
      if (block.type === "fallback") cb.onNotice(`${block.from.model} declined this turn; ${block.to.model} continued.`);
    });

    let message: BetaMessage;
    try {
      message = await stream.finalMessage();
      jsonRetries = 0;
    } catch (err) {
      // Only an unparseable streamed tool input is retried; API errors surface.
      if (err instanceof Anthropic.APIError || signal.aborted || jsonRetries++ >= 2) throw err;
      cb.onNotice("A tool call arrived malformed; retrying the step.");
      continue;
    }

    input += message.usage.input_tokens ?? 0;
    output += message.usage.output_tokens ?? 0;
    cached += message.usage.cache_read_input_tokens ?? 0;

    if (message.stop_reason === "refusal") {
      messages.push({ role: "assistant", content: message.content });
      cb.onNotice("The model declined this request. Try rephrasing it.");
      break;
    }
    if (message.stop_reason === "pause_turn") {
      messages.push({ role: "assistant", content: message.content });
      continue;
    }

    const toolUses = message.content.filter((b): b is Anthropic.Beta.Messages.BetaToolUseBlock => b.type === "tool_use");
    messages.push({ role: "assistant", content: message.content });
    if (message.stop_reason === "max_tokens") {
      cb.onNotice("The response hit the length limit. Ask Atelier to continue.");
      if (toolUses.length) messages.push({ role: "user", content: toolUses.map((t) => ({ type: "tool_result" as const, tool_use_id: t.id, is_error: true, content: "Not run: response was cut off." })) });
      break;
    }
    if (!toolUses.length) break;

    const results: ToolResult[] = toolUses.map((t) => {
      const { content, isError } = runLocalTool(t.name, t.input);
      const args = t.input as Record<string, unknown>;
      cb.onTool(t.name === "search_knowledge" ? `Searched knowledge: ${String(args.query ?? "")}` : `Read knowledge: ${String(args.id ?? "")}`);
      return { type: "tool_result", tool_use_id: t.id, content, is_error: isError || undefined };
    });
    messages.push({ role: "user", content: results });
  }

  return { usage: `${input.toLocaleString()} in (${cached.toLocaleString()} cached) / ${output.toLocaleString()} out` };
}
