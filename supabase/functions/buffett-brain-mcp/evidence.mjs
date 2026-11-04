/**
 * Deterministic public-only research retrieval. No live quotes or private data.
 * All returned source URLs originate in the committed knowledge/atlas.json.
 */
const ROOT = "https://github.com/kkfir13/warren-buffett-brain/blob/main/";
const clamp = (n, low, high) => Math.min(high, Math.max(low, n));
const terms = (s) => (String(s ?? "").toLowerCase().match(/[a-z0-9]+/g) ?? []);
const safeText = (s) => String(s ?? "").slice(0, 220);

export function sourceRecord(atlas, id) {
  return atlas.sources.find((s) => s.id === id) ?? null;
}

export function recordById(atlas, rawId) {
  const id = String(rawId ?? "").trim().slice(0, 120);
  if (!id) return null;
  const entry = atlas.entries.find((e) => e.id === id);
  if (!entry) {
    const src = sourceRecord(atlas, id);
    return src ? { recordType: "source", ...src, note: "A source link in the project is not proof its complete contents were ingested or read." } : null;
  }
  const linkedSources = (entry.sourceIds ?? [])
    .map((sid) => sourceRecord(atlas, sid))
    .filter(Boolean)
    .map((s) => ({ id: s.id, title: s.title, year: s.year ?? null, url: s.url, locator: s.locator ?? null, rights: s.rights ?? null }));
  const deepDiveUrl = typeof entry.deepDivePath === "string" && /^deep-dives\/[a-z0-9-]+\.md$/.test(entry.deepDivePath)
    ? ROOT + entry.deepDivePath : null;
  return {
    recordType: "research-note",
    id: entry.id, title: entry.title, year: entry.year, kind: entry.kind,
    companies: entry.companies ?? [], topics: entry.topics ?? [],
    summary: entry.summary, evidence: entry.evidence,
    interpretation: entry.interpretation, limitations: entry.limitations,
    verification: entry.verification, locator: entry.locator ?? null,
    speaker: entry.speaker ?? null, verbatimExcerpt: entry.verbatimExcerpt ?? null,
    sourceLinks: linkedSources, deepDiveUrl,
    researchUrl: ROOT + "knowledge/atlas.json",
    note: "Original paraphrase; external links point to source material, not copies. Check the original before claiming independent verification."
  };
}

export function searchEvidence(atlas, rawQuery, rawLimit = 5) {
  const query = String(rawQuery ?? "").trim().slice(0, 160);
  const tokens = terms(query).slice(0, 18);
  if (!tokens.length) return { query, total: 0, results: [], note: "Enter a company, investment decision, book, year, or principle." };
  const limit = clamp(Number.isFinite(Number(rawLimit)) ? Math.floor(Number(rawLimit)) : 5, 1, 10);
  const scored = atlas.entries.map((e) => {
    const title = String(e.title ?? "").toLowerCase();
    const companies = (e.companies ?? []).join(" ").toLowerCase();
    const topics = (e.topics ?? []).join(" ").toLowerCase();
    const explanation = [e.summary, e.evidence, e.interpretation, e.limitations].join(" ").toLowerCase();
    const year = String(e.year ?? "");
    const score = tokens.reduce((n, t) => n + (title.includes(t) ? 5 : 0)
      + (companies.includes(t) ? 4 : 0) + (topics.includes(t) ? 3 : 0)
      + (explanation.includes(t) ? 1 : 0) + (year.includes(t) ? 3 : 0), 0);
    return { e, score };
  }).filter((r) => r.score > 0).sort((a, b) => b.score - a.score || Number(b.e.year) - Number(a.e.year) || a.e.id.localeCompare(b.e.id));
  return {
    query, total: scored.length,
    results: scored.slice(0, limit).map(({ e }) => ({
      id: e.id, title: e.title, kind: e.kind, year: e.year,
      snippet: safeText(e.summary), sourceIds: e.sourceIds ?? [],
      sources: (e.sourceIds ?? []).map((sid) => sourceRecord(atlas, sid)).filter(Boolean)
        .map((s) => ({ title: s.title, url: s.url })),
      researchUrl: ROOT + "knowledge/atlas.json"
    })),
    note: "Search returns independently written, source-linked research notes, not full Berkshire letter text."
  };
}

export function coverage(atlas) {
  const counts = {};
  for (const e of atlas.entries) counts[e.kind] = (counts[e.kind] ?? 0) + 1;
  return {
    title: "Warren Buffett Brain", status: "independent open-source historical research",
    originalResearchNotes: atlas.entries.length, externalSourceLinks: atlas.sources.length,
    categories: counts,
    researchWebsite: "https://kkfir13.github.io/warren-buffett-brain/",
    sourceRepository: "https://github.com/kkfir13/warren-buffett-brain",
    notes: [
      "Source links do not imply complete source texts were ingested.",
      "Not affiliated with Warren Buffett or Berkshire Hathaway.",
      "No live stock prices, private portfolios, broker connections, or investment recommendations."
    ]
  };
}
