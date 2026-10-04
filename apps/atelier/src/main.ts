import "./styles.css";
import Anthropic from "@anthropic-ai/sdk";
import DOMPurify from "dompurify";
import { marked } from "marked";
import { runTurn } from "./claude";
import { knowledgeFiles, lensCards, readSection, search, vocabCards, type Card } from "./knowledge";
import {
  deleteConversation,
  getConversation,
  listConversations,
  loadSettings,
  newConversation,
  putConversation,
  saveSettings,
  toMarkdown,
  type Conversation,
  type Settings,
  type UiEntry,
} from "./store";

// ---------- tiny DOM helper ----------
type Attrs = Record<string, string | boolean | ((e: Event) => void) | undefined>;
function h<K extends keyof HTMLElementTagNameMap>(tag: K, attrs: Attrs = {}, ...kids: (Node | string | null | false)[]): HTMLElementTagNameMap[K] {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (v === undefined || v === false) continue;
    if (typeof v === "function") el.addEventListener(k.replace(/^on/, ""), v);
    else if (v === true) el.setAttribute(k, "");
    else if (k === "class") el.className = v;
    else el.setAttribute(k, v);
  }
  for (const kid of kids) if (kid !== null && kid !== false) el.append(kid);
  return el;
}
const md = (text: string) => {
  const div = h("div", { class: "md" });
  div.innerHTML = DOMPurify.sanitize(marked.parse(text, { async: false }) as string);
  div.querySelectorAll("a").forEach((a) => {
    a.target = "_blank";
    a.rel = "noopener noreferrer";
  });
  return div;
};

const ORBIT = `<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="13" fill="none" stroke="currentColor" stroke-width="3" stroke-dasharray="62 20" transform="rotate(-30 20 20)"/><circle cx="31" cy="11" r="5" fill="#C9A24B"/></svg>`;

// ---------- state ----------
let settings: Settings = loadSettings();
let tab: "studio" | "library" | "lenses" | "vocab" | "settings" = settings.apiKey ? "studio" : "settings";
let convo: Conversation = newConversation();
let sessions: Conversation[] = [];
let mode = "Consult";
let busy = false;
let abort: AbortController | null = null;
let pending: { kind: "image" | "pdf"; mediaType: string; data: string; preview: string; name: string }[] = [];
let draft = "";

const MODES: Record<string, string> = {
  Consult: "",
  Challenge: "Mode: Challenge. Steelman my idea, run at least two challenge modes, bring one perspective from another era or culture, then give me a stronger version.",
  Brand: "Mode: Brand. Work through the brand creation template. Ask me for anything critical you are missing first.",
  Campaign: "Mode: Campaign. Insight, idea as a verb, idea size, look and feel written down, executions across the funnel, and a variant system.",
  Avatar: "Mode: Avatar or mascot. Use the character template and finish with a prompt pack.",
  "3D": "Mode: 3D concept. Use the 3D concept template and finish with prompts for the tools I have.",
  Critique: "Mode: Critique. Follow the critique protocol on what I share, and end with the single change that would improve it most.",
  Research: "Mode: Research. Research this thoroughly with the knowledge base and the web. Cite every figure inline with its source tier.",
  Lens: "Mode: Lens. Look at this through three contrasting lenses (one era, one world culture, one discipline) and say what each one reveals.",
  Vocabulary: "Mode: Vocabulary. Teach me the precise terms for what is going on here, with examples and how to use each term in direction.",
};

const STARTERS = [
  { t: "Challenge my idea", d: "Paste a concept and get it steelmanned, stress-tested and rebuilt.", m: "Challenge", p: "Here's my idea: " },
  { t: "Build a brand", d: "From truths and positioning to palette, type, motif and voice.", m: "Brand", p: "I need a brand for " },
  { t: "Campaign concept", d: "Insight, verb, idea size, look and feel, executions.", m: "Campaign", p: "Campaign brief: " },
  { t: "Critique this", d: "Attach an ad, post, logo or site and get a director's read.", m: "Critique", p: "Critique this. Context: " },
  { t: "Design a mascot or avatar", d: "Character brief, expression sheet, prompt pack.", m: "Avatar", p: "Design a character for " },
  { t: "Through another lens", d: "See a brief through an era, a culture and a discipline.", m: "Lens", p: "Brief: " },
  { t: "Teach me the words", d: "Name what you're seeing so you can direct it.", m: "Vocabulary", p: "What are the terms for " },
  { t: "Research deep", d: "Cited research on a brand, artist, movement or platform.", m: "Research", p: "Research " },
];

// ---------- shell ----------
const app = document.getElementById("app")!;
const side = h("aside", { class: "side" });
const scrim = h("div", { class: "scrim", onclick: () => toggleSide(false) });
const main = h("main", { class: "main" });
app.append(side, scrim, main);
applyTheme();

function toggleSide(open: boolean) {
  side.classList.toggle("open", open);
  scrim.classList.toggle("open", open);
}

function applyTheme() {
  const t = localStorage.getItem("atelier.theme");
  if (t === "light" || t === "dark") document.documentElement.dataset.theme = t;
  else delete document.documentElement.dataset.theme;
}

async function refreshSessions() {
  sessions = await listConversations().catch(() => []);
  renderSide();
}

function renderSide() {
  const brand = h("div", { class: "brand" });
  brand.innerHTML = ORBIT;
  (brand.firstChild as SVGElement).style.color = "var(--ink)";
  brand.append(h("div", {}, h("h1", {}, "Atel", h("em", {}, "ier")), h("div", { class: "eyebrow" }, "Art direction agent")));

  const list = h("div", { class: "sessions" });
  const byProject = new Map<string, Conversation[]>();
  for (const s of sessions) byProject.set(s.project, [...(byProject.get(s.project) ?? []), s]);
  for (const [project, items] of byProject) {
    list.append(h("h3", { class: "eyebrow" }, project));
    for (const s of items) {
      list.append(
        h("button", { class: `session${s.id === convo.id ? " active" : ""}`, onclick: () => openSession(s.id), title: s.title }, s.title),
      );
    }
  }
  if (!sessions.length) list.append(h("p", { class: "eyebrow", style: "padding:6px" }, "Sessions you start are saved on this device."));

  side.replaceChildren(
    brand,
    h("button", { class: "primary", onclick: () => startNew() }, "+ New session"),
    list,
  );
}

function renderTop() {
  const tabs: [typeof tab, string][] = [
    ["studio", "Studio"],
    ["library", "Library"],
    ["lenses", "Lenses"],
    ["vocab", "Vocabulary"],
    ["settings", "Settings"],
  ];
  return h(
    "div",
    { class: "topbar" },
    h("button", { class: "menu", "aria-label": "Sessions", onclick: () => toggleSide(true) }, "☰"),
    h("nav", { class: "tabs" }, ...tabs.map(([k, label]) => h("button", { class: `tab${tab === k ? " on" : ""}`, onclick: () => go(k) }, label))),
  );
}

function go(t: typeof tab) {
  tab = t;
  render();
}

function render() {
  const view = h("div", { class: "view" });
  main.replaceChildren(renderTop(), view);
  if (tab === "studio") renderStudio(view);
  if (tab === "library") renderLibrary(view);
  if (tab === "lenses") renderLenses(view);
  if (tab === "vocab") renderVocab(view);
  if (tab === "settings") renderSettings(view);
}

// ---------- studio ----------
let logEl: HTMLElement;
let textarea: HTMLTextAreaElement;

function renderStudio(view: HTMLElement) {
  view.style.overflow = "hidden";
  const studio = h("div", { class: "studio" });
  logEl = h("div", { class: "log" });
  const inner = h("div", { class: "wrap" });
  logEl.append(inner);

  if (!convo.ui.length) {
    inner.append(
      h("div", { class: "empty" },
        h("div", { class: "eyebrow" }, "Bright Matter studio"),
        h("h2", {}, "What are we ", h("em", {}, "making"), " today?"),
        h("p", {}, "Bring a brief, a half-idea or a reference. Atelier will find the insight, size the idea, write the look and feel down, and push back where it should. It knows art and design history from cave painting to AI video, the science of advertising, and the vocabulary to direct any vendor."),
        h("div", { class: "starters" },
          ...STARTERS.map((s) =>
            h("button", { class: "starter", onclick: () => { mode = s.m; draft = s.p; render(); textarea.focus(); } }, h("b", {}, s.t), h("span", {}, s.d)),
          ),
        ),
      ),
    );
  } else {
    inner.append(
      h("div", { class: "row", style: "justify-content:space-between" },
        h("div", { class: "eyebrow" }, `${convo.project} · ${convo.title}`),
        h("div", { class: "row" },
          h("button", { class: "ghost", onclick: () => renameSession() }, "Rename"),
          h("button", { class: "ghost", onclick: () => exportSession() }, "Export .md"),
          h("button", { class: "ghost", onclick: () => removeSession() }, "Delete"),
        ),
      ),
    );
    for (const e of convo.ui) inner.append(renderEntry(e));
  }

  // composer
  const modes = h("div", { class: "modes" }, ...Object.keys(MODES).map((m) => h("button", { class: `mode${m === mode ? " on" : ""}`, onclick: () => { mode = m; draft = textarea.value; render(); } }, m)));
  const pendingRow = h("div", { class: "pending" }, ...pending.map((p, i) =>
    h("div", { class: "thumb" },
      p.kind === "image" ? h("img", { src: p.preview, alt: p.name }) : h("div", { class: "pdf" }, `PDF · ${p.name.slice(0, 18)}`),
      h("button", { "aria-label": "Remove", onclick: () => { pending.splice(i, 1); draft = textarea.value; render(); } }, "×"),
    ),
  ));
  const file = h("input", { type: "file", accept: "image/*,application/pdf", multiple: true, style: "display:none", onchange: (e) => addFiles((e.target as HTMLInputElement).files) });
  textarea = h("textarea", { rows: "1", placeholder: settings.apiKey ? "Describe the project, paste an idea, or attach work…" : "Add your API key in Settings to start", oninput: autosize, onkeydown: onKey });
  textarea.value = draft;
  const sendBtn = busy
    ? h("button", { class: "primary", onclick: () => abort?.abort() }, "Stop")
    : h("button", { class: "primary", onclick: () => send(), disabled: !settings.apiKey }, "Send");
  const composer = h("div", { class: "composer" },
    modes,
    pending.length ? pendingRow : null,
    h("div", { class: "box" }, h("button", { class: "attach", "aria-label": "Attach image or PDF", onclick: () => file.click() }, "＋"), textarea, sendBtn, file),
  );
  studio.append(logEl, composer);
  view.append(studio);
  autosize();
  logEl.scrollTop = logEl.scrollHeight;
  textarea.addEventListener("paste", (e) => {
    const files = (e as ClipboardEvent).clipboardData?.files;
    if (files?.length) addFiles(files);
  });
}

function autosize() {
  if (!textarea) return;
  textarea.style.height = "auto";
  textarea.style.height = `${Math.min(textarea.scrollHeight, window.innerHeight * 0.4)}px`;
}

function onKey(e: Event) {
  const k = e as KeyboardEvent;
  if (k.key === "Enter" && !k.shiftKey && !k.isComposing && window.matchMedia("(pointer:fine)").matches) {
    k.preventDefault();
    send();
  }
}

function renderEntry(e: UiEntry): HTMLElement {
  if (e.role === "notice") return h("div", { class: "msg notice" }, e.text);
  if (e.role === "user") {
    return h("div", { class: "msg user" },
      e.images?.length ? h("div", { class: "imgs" }, ...e.images.map((src) => h("img", { src, alt: "attachment" }))) : null,
      h("div", { class: "bubble" }, e.text),
    );
  }
  const box = h("div", { class: "msg assistant" });
  box.append(h("div", { class: "who" }, h("span", { class: "dot" }), h("span", { class: "eyebrow" }, "Atelier")));
  if (settings.showThinking && e.thinking) {
    box.append(h("details", { class: "think" }, h("summary", {}, "How Atelier thought about it"), h("div", {}, e.thinking)));
  }
  if (e.tools?.length) box.append(h("div", { class: "tools" }, ...e.tools.map((t) => h("span", { class: "chip" }, t))));
  box.append(md(e.text || ""));
  if (e.sources?.length) {
    const seen = new Set<string>();
    const uniq = e.sources.filter((s) => (seen.has(s.url) ? false : (seen.add(s.url), true))).slice(0, 12);
    box.append(h("div", { class: "sources" }, h("span", { class: "eyebrow" }, "Sources  "), ...uniq.map((s) => h("a", { href: s.url, target: "_blank", rel: "noopener noreferrer" }, s.title || new URL(s.url).hostname))));
  }
  if (e.usage) box.append(h("div", { class: "usage" }, e.usage));
  return box;
}

async function addFiles(list: FileList | null) {
  if (!list) return;
  for (const f of Array.from(list)) {
    if (f.type === "application/pdf") {
      const data = await fileToBase64(f);
      pending.push({ kind: "pdf", mediaType: "application/pdf", data, preview: "", name: f.name });
    } else if (f.type.startsWith("image/")) {
      const { data, url } = await downscale(f);
      pending.push({ kind: "image", mediaType: "image/jpeg", data, preview: url, name: f.name });
    }
  }
  draft = textarea?.value ?? draft;
  render();
}

function fileToBase64(f: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const r = new FileReader();
    r.onload = () => resolve(String(r.result).split(",")[1]);
    r.onerror = () => reject(r.error);
    r.readAsDataURL(f);
  });
}

async function downscale(f: File): Promise<{ data: string; url: string }> {
  const bmp = await createImageBitmap(f);
  const scale = Math.min(1, 1568 / Math.max(bmp.width, bmp.height));
  const c = document.createElement("canvas");
  c.width = Math.round(bmp.width * scale);
  c.height = Math.round(bmp.height * scale);
  const ctx = c.getContext("2d")!;
  ctx.fillStyle = "#ffffff";
  ctx.fillRect(0, 0, c.width, c.height);
  ctx.drawImage(bmp, 0, 0, c.width, c.height);
  const url = c.toDataURL("image/jpeg", 0.88);
  return { data: url.split(",")[1], url };
}

async function send() {
  if (busy || !settings.apiKey) return;
  const text = textarea.value.trim();
  if (!text && !pending.length) return;

  const prefix = MODES[mode] ? `${MODES[mode]}\n\n` : "";
  const dateLine = convo.messages.length === 0 ? `(Today is ${new Date().toDateString()}.)\n\n` : "";
  type Block = Anthropic.Beta.Messages.BetaContentBlockParam;
  const content: Block[] = [
    ...pending.map((p): Block =>
      p.kind === "image"
        ? { type: "image", source: { type: "base64", media_type: "image/jpeg", data: p.data } }
        : { type: "document", source: { type: "base64", media_type: "application/pdf", data: p.data } },
    ),
    { type: "text", text: `${dateLine}${prefix}${text || "(see attachment)"}` },
  ];

  if (convo.messages.length === 0) convo.title = text.split(/\s+/).slice(0, 7).join(" ").slice(0, 60) || "Session";
  const historyLength = convo.messages.length;
  convo.messages.push({ role: "user", content });
  convo.ui.push({ role: "user", text: mode !== "Consult" ? `[${mode}] ${text}` : text, images: pending.filter((p) => p.kind === "image").map((p) => p.preview) });
  const reply: UiEntry = { role: "assistant", text: "", thinking: "", tools: [], sources: [] };
  convo.ui.push(reply);
  const sentAttachments = pending;
  pending = [];
  draft = "";
  busy = true;
  abort = new AbortController();
  render();

  // Live node for the streaming reply.
  const inner = logEl.firstElementChild as HTMLElement;
  let live = inner.lastElementChild as HTMLElement;
  let queued = false;
  const repaint = () => {
    if (queued) return;
    queued = true;
    requestAnimationFrame(() => {
      queued = false;
      const fresh = renderEntry(reply);
      fresh.querySelector(".md")?.classList.add("cursor");
      live.replaceWith(fresh);
      live = fresh;
      const nearBottom = logEl.scrollHeight - logEl.scrollTop - logEl.clientHeight < 160;
      if (nearBottom) logEl.scrollTop = logEl.scrollHeight;
    });
  };

  try {
    const { usage } = await runTurn(settings, convo.messages, {
      onText: (d) => { reply.text += d; repaint(); },
      onThinking: (d) => { reply.thinking += d; repaint(); },
      onTool: (label) => { reply.tools!.push(label); repaint(); },
      onSource: (s) => { reply.sources!.push(s); },
      onNotice: (t) => { convo.ui.push({ role: "notice", text: t }); },
    }, abort.signal);
    reply.usage = usage;
  } catch (err) {
    convo.ui.push({ role: "notice", text: `${errorText(err)} Your message is back in the box to resend.` });
    // Keep the history valid: drop this unfinished turn (it is the tail, so
    // nothing later depends on it) and put the text back in the composer.
    convo.messages.length = historyLength;
    draft = text;
    pending = sentAttachments;
  } finally {
    if (!reply.text && !reply.tools?.length) convo.ui.splice(convo.ui.indexOf(reply), 1);
    busy = false;
    abort = null;
    if (!draft) mode = "Consult";
    convo.updated = Date.now();
    await putConversation(convo).catch(() => undefined);
    await refreshSessions();
    render();
  }
}

function errorText(err: unknown): string {
  if (err instanceof Anthropic.APIUserAbortError) return "Stopped.";
  if (err instanceof Anthropic.AuthenticationError) return "The API key was rejected. Check it in Settings.";
  if (err instanceof Anthropic.RateLimitError) return "Rate limited. Wait a moment and try again.";
  if (err instanceof Anthropic.APIConnectionError) return "Could not reach the Claude API. Check your connection.";
  if (err instanceof Anthropic.APIError) return `Claude API error ${err.status ?? ""}: ${err.message}`;
  return `Something went wrong: ${err instanceof Error ? err.message : String(err)}`;
}

async function startNew(project?: string) {
  convo = newConversation(project ?? convo.project ?? "General");
  mode = "Consult";
  pending = [];
  draft = "";
  tab = "studio";
  toggleSide(false);
  renderSide();
  render();
}

async function openSession(id: string) {
  const c = await getConversation(id);
  if (!c) return;
  convo = c;
  tab = "studio";
  toggleSide(false);
  renderSide();
  render();
}

async function renameSession() {
  const title = prompt("Session title", convo.title);
  if (title === null) return;
  const project = prompt("Project (groups sessions in the sidebar)", convo.project);
  convo.title = title.trim() || convo.title;
  convo.project = project?.trim() || convo.project;
  await putConversation(convo);
  await refreshSessions();
  render();
}

function exportSession() {
  const blob = new Blob([toMarkdown(convo)], { type: "text/markdown" });
  const a = h("a", { href: URL.createObjectURL(blob), download: `${convo.title.replace(/[^\w]+/g, "-").toLowerCase()}.md` });
  a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
}

async function removeSession() {
  if (!confirm(`Delete "${convo.title}"? This can't be undone.`)) return;
  await deleteConversation(convo.id);
  await refreshSessions();
  startNew();
}

/** Put text in the composer and switch to the studio. */
function useInStudio(text: string, m = "Consult") {
  mode = m;
  draft = text;
  tab = "studio";
  render();
  textarea.focus();
}

// ---------- library ----------
let libQuery = "";
let libOpen: { title: string; text: string } | null = null;

function renderLibrary(view: HTMLElement) {
  const wrap = h("div", { class: "wrap" });
  const input = h("input", { class: "lib-search", type: "search", placeholder: "Search the knowledge base: chiaroscuro, mental availability, Hockney joiner…", value: libQuery });
  const results = h("div");
  const paint = () => {
    results.replaceChildren();
    if (libOpen) {
      results.append(
        h("div", { class: "row", style: "margin:18px 0" },
          h("button", { class: "ghost", onclick: () => { libOpen = null; paint(); } }, "← Back"),
          h("button", { class: "ghost", onclick: () => useInStudio(`From the knowledge base, "${libOpen!.title}": `) }, "Ask Atelier about this"),
        ),
        md(libOpen.text),
      );
      return;
    }
    if (libQuery.trim()) {
      const hits = search(libQuery, 20);
      if (!hits.length) results.append(h("p", {}, "No matches."));
      for (const hit of hits) {
        results.append(h("div", { class: "hit" },
          h("button", { onclick: () => { libOpen = { title: hit.heading, text: readSection(hit.id) ?? "" }; paint(); } }, hit.heading),
          h("div", { class: "eyebrow" }, hit.file),
          h("div", {}, hit.snippet),
        ));
      }
      return;
    }
    results.append(h("div", { class: "files" }, ...knowledgeFiles.map((f) =>
      h("button", { class: "file", onclick: () => { libOpen = { title: f.title, text: f.text }; paint(); } },
        h("span", { class: "eyebrow" }, f.slug.slice(0, 2)), h("b", {}, f.title), h("span", { class: "eyebrow" }, `${Math.round(f.text.split(/\s+/).length / 100) / 10}k words`)),
    )));
  };
  input.addEventListener("input", () => { libQuery = input.value; libOpen = null; paint(); });
  wrap.append(h("div", { class: "eyebrow" }, "Knowledge base"), h("h2", { style: "font:800 32px/1.1 var(--display);color:var(--ink);letter-spacing:-.03em" }, "The library"), input, results);
  paint();
  view.append(wrap);
}

// ---------- lenses ----------
function renderLenses(view: HTMLElement) {
  const cards = lensCards();
  const groups = [...new Set(cards.map((c) => c.group))];
  let group = "All";
  let card: Card | undefined = cards[Math.floor(Math.random() * cards.length)];
  const wrap = h("div", { class: "wrap" });
  const holder = h("div");
  const paint = () => {
    holder.replaceChildren(
      h("div", { class: "row" }, ...["All", ...groups].map((g) => h("button", { class: `mode${g === group ? " on" : ""}`, onclick: () => { group = g; draw(); } }, g))),
      card
        ? h("div", { class: "card" },
            h("div", { class: "eyebrow" }, card.group),
            h("h2", {}, card.term),
            md(card.body),
            h("div", { class: "row", style: "margin-top:18px" },
              h("button", { class: "primary", onclick: () => useInStudio(`Look at my brief through this lens: ${card!.term}. ${card!.body}\n\nBrief: `, "Lens") }, "Use this lens"),
              h("button", { class: "ghost", onclick: draw }, "Draw another"),
            ),
          )
        : h("p", {}, "No lens cards found in the knowledge base."),
    );
  };
  const draw = () => {
    const pool = group === "All" ? cards : cards.filter((c) => c.group === group);
    card = pool[Math.floor(Math.random() * pool.length)];
    paint();
  };
  wrap.append(h("div", { class: "eyebrow" }, "Perspective deck"), h("h2", { style: "font:800 32px/1.1 var(--display);color:var(--ink);letter-spacing:-.03em" }, "Draw a lens"), h("p", {}, `${cards.length} eras, cultures, audiences and disciplines to throw at a brief.`), holder);
  paint();
  view.append(wrap);
}

// ---------- vocabulary ----------
function renderVocab(view: HTMLElement) {
  const cards = vocabCards();
  const groups = [...new Set(cards.map((c) => c.group))];
  let group = "All";
  let i = Math.floor(Math.random() * cards.length);
  let pool = cards;
  let revealed = false;
  const wrap = h("div", { class: "wrap" });
  const holder = h("div");
  const paint = () => {
    const c = pool[i % pool.length];
    holder.replaceChildren(
      h("div", { class: "row" }, ...["All", ...groups].map((g) => h("button", { class: `mode${g === group ? " on" : ""}`, onclick: () => { group = g; pool = g === "All" ? cards : cards.filter((x) => x.group === g); i = 0; revealed = false; paint(); } }, g))),
      c
        ? h("div", { class: "card" },
            h("div", { class: "eyebrow" }, `${c.group} · ${(i % pool.length) + 1} of ${pool.length}`),
            h("h2", {}, c.term),
            revealed ? md(c.body) : h("p", { class: "eyebrow" }, "Say it in your own words, then reveal."),
            h("div", { class: "row", style: "margin-top:18px" },
              revealed
                ? h("button", { class: "primary", onclick: () => { i = Math.floor(Math.random() * pool.length); revealed = false; paint(); } }, "Next term")
                : h("button", { class: "primary", onclick: () => { revealed = true; paint(); } }, "Reveal"),
              h("button", { class: "ghost", onclick: () => useInStudio(`Show me three strong examples of "${c.term}" in advertising or design (different eras or regions), and how I'd direct a photographer, designer or AI tool to use it.`, "Vocabulary") }, "Examples from Atelier"),
            ),
          )
        : h("p", {}, "No vocabulary found."),
    );
  };
  wrap.append(h("div", { class: "eyebrow" }, "Drill"), h("h2", { style: "font:800 32px/1.1 var(--display);color:var(--ink);letter-spacing:-.03em" }, "Visual vocabulary"), holder);
  paint();
  view.append(wrap);
}

// ---------- settings ----------
function renderSettings(view: HTMLElement) {
  const s = { ...settings };
  const save = () => { settings = s; saveSettings(settings); };
  const field = (label: string, el: HTMLElement, note?: string) => h("label", { class: "field" }, h("span", { class: "eyebrow" }, label), el, note ? h("small", {}, note) : null);
  const key = h("input", { type: "password", autocomplete: "off", placeholder: "sk-ant-…", value: s.apiKey, oninput: (e) => { s.apiKey = (e.target as HTMLInputElement).value.trim(); save(); } });
  const model = h("select", { onchange: (e) => { s.model = (e.target as HTMLSelectElement).value as Settings["model"]; save(); } },
    h("option", { value: "claude-opus-5-5", selected: s.model === "claude-opus-5-5" }, "Claude Opus 5.5 (deepest)"),
    h("option", { value: "claude-sonnet-5-5", selected: s.model === "claude-sonnet-5-5" }, "Claude Sonnet 5.5 (faster)"),
  );
  const effort = h("select", { onchange: (e) => { s.effort = (e.target as HTMLSelectElement).value as Settings["effort"]; save(); } },
    ...(["low", "medium", "high", "xhigh", "max"] as const).map((v) => h("option", { value: v, selected: s.effort === v }, v)),
  );
  const check = (label: string, keyName: "webSearch" | "showThinking") =>
    h("label", { class: "toggle" }, h("input", { type: "checkbox", checked: s[keyName], onchange: (e) => { s[keyName] = (e.target as HTMLInputElement).checked; save(); } }), label);
  const theme = h("select", { onchange: (e) => { const v = (e.target as HTMLSelectElement).value; try { if (v === "system") localStorage.removeItem("atelier.theme"); else localStorage.setItem("atelier.theme", v); } catch { /* ignore */ } applyTheme(); } },
    ...["system", "light", "dark"].map((v) => h("option", { value: v, selected: (localStorage.getItem("atelier.theme") ?? "system") === v }, v)),
  );

  view.append(h("div", { class: "wrap" },
    h("div", { class: "eyebrow" }, "Settings"),
    h("h2", { style: "font:800 32px/1.1 var(--display);color:var(--ink);letter-spacing:-.03em" }, "Set up Atelier"),
    field("Anthropic API key", key, "Stored only in this browser on this device and sent only to api.anthropic.com. Create one at console.anthropic.com. Use a key with a spend limit."),
    field("Model", model),
    field("Effort", effort, "Higher effort thinks longer and costs more. High is a good default; use max for big brand or campaign work."),
    check("Web search and page reading (for current facts and research)", "webSearch"),
    check("Show Atelier's thinking summary", "showThinking"),
    field("Theme", theme),
    h("div", { class: "row", style: "margin-top:12px" },
      h("button", { class: "primary", onclick: () => go("studio") }, "Done"),
      h("button", { class: "ghost", onclick: exportAll }, "Export all sessions (JSON)"),
    ),
    h("p", { class: "eyebrow", style: "margin-top:28px" }, `Knowledge base: ${knowledgeFiles.length} files bundled with this build.`),
  ));
}

async function exportAll() {
  const all = await listConversations();
  const blob = new Blob([JSON.stringify(all, null, 1)], { type: "application/json" });
  const a = h("a", { href: URL.createObjectURL(blob), download: `atelier-sessions-${new Date().toISOString().slice(0, 10)}.json` });
  a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
}

// ---------- boot ----------
refreshSessions().then(render);
if ("serviceWorker" in navigator && import.meta.env.PROD) {
  navigator.serviceWorker.register("./sw.js").catch(() => undefined);
}
