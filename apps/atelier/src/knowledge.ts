// Knowledge base: the markdown files in ClaudeSkills/art-director, bundled at
// build time and split into H2 sections for search and on-demand reading.

import agentBrief from "../../../art-director/AGENT.md?raw";

const files = import.meta.glob("../../../art-director/knowledge/*.md", {
  query: "?raw",
  import: "default",
  eager: true,
}) as Record<string, string>;

export interface KnowledgeFile {
  slug: string; // e.g. "05-visual-vocabulary"
  title: string; // first H1
  text: string;
}

export interface Section {
  id: string; // slug#index
  slug: string;
  fileTitle: string;
  heading: string;
  text: string;
  tokens: string[];
}

export const AGENT_BRIEF = agentBrief;

export const knowledgeFiles: KnowledgeFile[] = Object.entries(files)
  .map(([path, text]) => {
    const slug = path.split("/").pop()!.replace(/\.md$/, "");
    const title = text.match(/^#\s+(.+)$/m)?.[1]?.trim() ?? slug;
    return { slug, title, text };
  })
  .sort((a, b) => a.slug.localeCompare(b.slug));

const STOP = new Set(
  "a an and are as at be but by for from has have in into is it its of on or that the their this to was were will with what when how why who which your you our we not can".split(
    " ",
  ),
);

export function tokenize(s: string): string[] {
  return s
    .toLowerCase()
    .normalize("NFKD")
    .replace(/[̀-ͯ]/g, "")
    .split(/[^a-z0-9]+/)
    .filter((t) => t.length > 1 && !STOP.has(t));
}

function splitSections(file: KnowledgeFile): Section[] {
  const out: Section[] = [];
  const lines = file.text.split("\n");
  let heading = file.title;
  let buf: string[] = [];
  const flush = () => {
    const text = buf.join("\n").trim();
    if (text.length > 40) {
      // Long sections are split again at H3 so search hits stay focused.
      const parts = text.length > 9000 ? text.split(/\n(?=### )/) : [text];
      for (const part of parts) {
        const sub = part.match(/^###\s+(.+)$/m)?.[1];
        const h = sub && parts.length > 1 ? `${heading} / ${sub}` : heading;
        out.push({
          id: `${file.slug}#${out.length}`,
          slug: file.slug,
          fileTitle: file.title,
          heading: h,
          text: part,
          tokens: tokenize(`${h} ${h} ${part}`),
        });
      }
    }
    buf = [];
  };
  for (const line of lines) {
    const m = line.match(/^##\s+(.+)$/);
    if (m) {
      flush();
      heading = m[1].trim();
    }
    buf.push(line);
  }
  flush();
  return out;
}

export const sections: Section[] = knowledgeFiles.flatMap(splitSections);

// BM25 over sections.
const N = sections.length;
const avgLen = sections.reduce((s, x) => s + x.tokens.length, 0) / Math.max(N, 1);
const df = new Map<string, number>();
const tf: Map<string, number>[] = sections.map((s) => {
  const m = new Map<string, number>();
  for (const t of s.tokens) m.set(t, (m.get(t) ?? 0) + 1);
  for (const t of m.keys()) df.set(t, (df.get(t) ?? 0) + 1);
  return m;
});

export interface SearchHit {
  id: string;
  file: string;
  heading: string;
  snippet: string;
  score: number;
}

export function search(query: string, limit = 6): SearchHit[] {
  const q = [...new Set(tokenize(query))];
  if (!q.length) return [];
  const k1 = 1.4;
  const b = 0.75;
  const scored = sections.map((s, i) => {
    let score = 0;
    for (const t of q) {
      const f = tf[i].get(t);
      if (!f) continue;
      const idf = Math.log(1 + (N - (df.get(t) ?? 0) + 0.5) / ((df.get(t) ?? 0) + 0.5));
      score += (idf * (f * (k1 + 1))) / (f + k1 * (1 - b + (b * s.tokens.length) / avgLen));
    }
    // Exact phrase bonus.
    if (q.length > 1 && s.text.toLowerCase().includes(query.toLowerCase().trim())) score *= 1.5;
    return { s, score };
  });
  return scored
    .filter((x) => x.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, limit)
    .map(({ s, score }) => ({
      id: s.id,
      file: s.slug,
      heading: s.heading,
      snippet: snippet(s.text, q),
      score: Math.round(score * 100) / 100,
    }));
}

function snippet(text: string, q: string[]): string {
  const lower = text.toLowerCase();
  let pos = -1;
  for (const t of q) {
    pos = lower.indexOf(t);
    if (pos >= 0) break;
  }
  const start = Math.max(0, pos - 160);
  return (start > 0 ? "..." : "") + text.slice(start, start + 420).replace(/\s+/g, " ").trim() + "...";
}

export function readSection(id: string, maxChars = 14000): string | null {
  const s = sections.find((x) => x.id === id);
  if (!s) return null;
  const body = s.text.length > maxChars ? s.text.slice(0, maxChars) + "\n[section truncated]" : s.text;
  return `FILE: ${s.slug} (${s.fileTitle})\nSECTION: ${s.heading}\n\n${body}`;
}

/** Table of contents the model sees in its system prompt. */
export function catalog(): string {
  return knowledgeFiles
    .map((f) => {
      const heads = sections.filter((s) => s.slug === f.slug).map((s) => `  - [${s.id}] ${s.heading}`);
      return `- ${f.slug}: ${f.title}\n${heads.join("\n")}`;
    })
    .join("\n");
}

/** Files embedded in full in the system prompt (the always-on core). */
export const CORE_SLUGS = ["01-jason-swet-study", "05-visual-vocabulary", "11-methods-lenses-and-templates"];

export function coreText(): string {
  return knowledgeFiles
    .filter((f) => CORE_SLUGS.includes(f.slug))
    .map((f) => `<knowledge_file name="${f.slug}">\n${f.text}\n</knowledge_file>`)
    .join("\n\n");
}

// ---- Lens deck and vocabulary cards, parsed from the knowledge files ----

export interface Card {
  group: string;
  term: string;
  body: string;
}

function parseBoldBullets(text: string, groupFrom: RegExp): Card[] {
  const cards: Card[] = [];
  let group = "";
  for (const line of text.split("\n")) {
    const g = line.match(groupFrom);
    if (g) group = g[1].replace(/\s*\(.*\)\s*$/, "").trim();
    const m = line.match(/^- \*\*(.+?)\*\*[:\s]*(.*)$/);
    if (m && group) cards.push({ group, term: m[1].replace(/[:*]+$/, "").trim(), body: m[2].trim() });
  }
  return cards;
}

export function lensCards(): Card[] {
  const f = knowledgeFiles.find((x) => x.slug.startsWith("11-"));
  if (!f) return [];
  const partD = f.text.split(/^## Part D/m)[1]?.split(/^## Part E/m)[0] ?? "";
  return parseBoldBullets(partD, /^###\s+(.+)$/);
}

export function vocabCards(): Card[] {
  const f = knowledgeFiles.find((x) => x.slug.startsWith("05-"));
  if (!f) return [];
  return parseBoldBullets(f.text, /^##\s+\d+\.\s+(.+)$/).filter((c) => c.body.length > 0);
}
