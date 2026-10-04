// Local persistence: conversations in IndexedDB (they can hold images),
// settings in localStorage. Nothing leaves the device except API calls.

import type Anthropic from "@anthropic-ai/sdk";

export type ApiMessage = Anthropic.Beta.Messages.BetaMessageParam;

export interface UiEntry {
  role: "user" | "assistant" | "notice";
  text: string;
  thinking?: string;
  tools?: string[]; // short labels of tool activity
  sources?: { title: string; url: string }[];
  images?: string[]; // data URLs, user uploads
  usage?: string;
}

export interface Conversation {
  id: string;
  title: string;
  project: string;
  created: number;
  updated: number;
  messages: ApiMessage[]; // exact API history, append-only
  ui: UiEntry[];
}

export interface Settings {
  apiKey: string;
  model: "claude-opus-5-5" | "claude-sonnet-5-5";
  effort: "low" | "medium" | "high" | "xhigh" | "max";
  webSearch: boolean;
  showThinking: boolean;
}

const SETTINGS_KEY = "atelier.settings";
const DEFAULTS: Settings = {
  apiKey: "",
  model: "claude-opus-5-5",
  effort: "high",
  webSearch: true,
  showThinking: true,
};

export function loadSettings(): Settings {
  try {
    return { ...DEFAULTS, ...JSON.parse(localStorage.getItem(SETTINGS_KEY) ?? "{}") };
  } catch {
    return { ...DEFAULTS };
  }
}

export function saveSettings(s: Settings) {
  try {
    localStorage.setItem(SETTINGS_KEY, JSON.stringify(s));
  } catch {
    /* private mode: settings live for this session only */
  }
}

let dbp: Promise<IDBDatabase> | null = null;
function db(): Promise<IDBDatabase> {
  dbp ??= new Promise((resolve, reject) => {
    const req = indexedDB.open("atelier", 1);
    req.onupgradeneeded = () => req.result.createObjectStore("conversations", { keyPath: "id" });
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
  return dbp;
}

async function tx<T>(mode: IDBTransactionMode, fn: (s: IDBObjectStore) => IDBRequest<T>): Promise<T> {
  const d = await db();
  return new Promise((resolve, reject) => {
    const req = fn(d.transaction("conversations", mode).objectStore("conversations"));
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

export const listConversations = async () =>
  (await tx<Conversation[]>("readonly", (s) => s.getAll())).sort((a, b) => b.updated - a.updated);
export const getConversation = (id: string) => tx<Conversation | undefined>("readonly", (s) => s.get(id));
export const putConversation = (c: Conversation) => tx("readwrite", (s) => s.put(c));
export const deleteConversation = (id: string) => tx("readwrite", (s) => s.delete(id));

export function newConversation(project = "General"): Conversation {
  const now = Date.now();
  return { id: crypto.randomUUID(), title: "New session", project, created: now, updated: now, messages: [], ui: [] };
}

export function toMarkdown(c: Conversation): string {
  const lines = [`# ${c.title}`, ``, `Project: ${c.project}  `, `Started: ${new Date(c.created).toLocaleString()}`, ``];
  for (const e of c.ui) {
    if (e.role === "notice") continue;
    lines.push(`## ${e.role === "user" ? "Shannon" : "Atelier"}`, "", e.text, "");
    if (e.sources?.length) {
      lines.push("Sources:", ...e.sources.map((s) => `- [${s.title}](${s.url})`), "");
    }
  }
  return lines.join("\n");
}
