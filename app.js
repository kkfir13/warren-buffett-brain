"use strict";
// Source-linked search, intentionally deterministic, local and dependency-free.
const byId = id => document.getElementById(id);
const node = (tag, className = "", text = "") => {
  const element = document.createElement(tag);
  if (className) element.className = className;
  element.textContent = String(text);
  return element;
};
const labels = {
  decision: "Investment decision", mistake: "Admitted mistake",
  principle: "Investment principle", book: "Book & influence",
  interview: "Original interview", statement: "Attributed statement"
};
let atlas = null, activeKind = "all", query = "", visible = 10, matching = [], inputTimer;
const tokens = value => String(value || "").toLowerCase().match(/[a-z0-9]+/g) || [];
const sourceIndex = () => new Map(atlas.sources.map(source => [source.id, source]));

function rankedEntries() {
  const parts = tokens(query);
  return atlas.entries.filter(entry => activeKind === "all" || entry.kind === activeKind)
    .map(entry => {
      const title = entry.title.toLowerCase();
      const people = entry.companies.join(" ").toLowerCase();
      const topics = entry.topics.join(" ").toLowerCase();
      const body = [entry.summary, entry.evidence, entry.interpretation, entry.limitations].join(" ").toLowerCase();
      const score = parts.length ? parts.reduce((sum, part) => sum +
        (title.includes(part) ? 5 : 0) + (people.includes(part) ? 4 : 0) +
        (topics.includes(part) ? 3 : 0) + (body.includes(part) ? 1 : 0) +
        (String(entry.year).includes(part) ? 3 : 0), 0) : 1;
      return { entry, score };
    })
    .filter(item => item.score > 0)
    .sort((a, b) => b.score - a.score || b.entry.year - a.entry.year || a.entry.id.localeCompare(b.entry.id))
    .map(item => item.entry);
}

function evidenceSection(title, text) {
  const section = node("section", "evidence-block");
  section.append(node("h4", "", title), node("p", "", text));
  return section;
}
function createRecord(entry, position) {
  const wrapper = node("article", "record");
  const stamp = node("div", "record-stamp");
  stamp.append(node("span", "stamp-year", entry.year), node("span", "stamp-index", "RECORD " + String(position + 1).padStart(2, "0")));
  const contents = node("div", "record-contents");
  const kind = node("span", "record-type", labels[entry.kind] || entry.kind);
  const heading = node("h3", "record-title", entry.title);
  const synopsis = node("p", "record-summary", entry.summary);
  contents.append(kind, heading);
  if (entry.verbatimExcerpt && entry.speaker) {
    const quote = node("blockquote", "record-quote", "“" + entry.verbatimExcerpt + "”");
    quote.append(node("cite", "", entry.speaker + " · " + entry.year));
    contents.append(quote);
  }
  contents.append(synopsis);
  const disclosure = node("details", "record-disclosure");
  const toggle = node("summary", "", "Read the evidence");
  toggle.append(node("span", "toggle-arrow", "↗"));
  disclosure.append(toggle);
  const panel = node("div", "evidence-panel");
  panel.append(evidenceSection("Documented evidence", entry.evidence),
    evidenceSection("Our interpretation", entry.interpretation),
    evidenceSection("Limits of the record", entry.limitations));
  if (entry.locator) panel.append(node("p", "record-locator", "Find in original: " + entry.locator));
  const sources = node("div", "source-group");
  sources.append(node("h4", "", "ORIGINAL SOURCES"));
  const index = sourceIndex();
  for (const id of entry.sourceIds) {
    const source = index.get(id);
    if (!source) continue;
    const a = node("a", "", source.title + " ↗");
    a.href = source.url; a.target = "_blank"; a.rel = "noopener noreferrer";
    sources.append(a);
  }
  panel.append(sources);
  if (entry.deepDivePath && /^deep-dives\/[a-z0-9-]+\.md$/.test(entry.deepDivePath)) {
    const slug = entry.deepDivePath.slice("deep-dives/".length).replace(/\.md$/, "");
    const deep = node("a", "deep-link", "Read the complete case study ↗");
    deep.href = "./cases/" + slug + "/";
    panel.append(deep);
  }
  disclosure.append(panel);
  contents.append(disclosure);
  wrapper.append(stamp, contents);
  return wrapper;
}
function render() {
  if (!atlas) return;
  matching = rankedEntries();
  const container = byId("cards");
  container.replaceChildren();
  for (const [index, entry] of matching.slice(0, visible).entries()) {
    container.append(createRecord(entry, index));
  }
  byId("status").textContent = matching.length
    ? matching.length + " source-linked " + (matching.length === 1 ? "record" : "records") + (query ? " matching your search" : " in the archive")
    : "No source-linked record matches this search. Try another name, year or principle.";
  const more = byId("more");
  more.hidden = matching.length <= visible;
  more.textContent = matching.length > visible
    ? "Show " + Math.min(10, matching.length - visible) + " more records ↓" : "All records shown";
}
function setQuery(value, updateUrl = true) {
  query = value.trim(); visible = 10;
  if (updateUrl) {
    const params = new URLSearchParams(location.search);
    if (query) params.set("q", query); else params.delete("q");
    const search = params.toString();
    history.replaceState(null, "", location.pathname + (search ? "?" + search : "") + location.hash);
  }
  render();
}
function showKind(value) {
  activeKind = value;
  visible = 10;
  document.querySelectorAll("[data-kind]").forEach(button => {
    const selected = button.dataset.kind === value;
    button.classList.toggle("active", selected);
    button.setAttribute("aria-pressed", String(selected));
  });
  render();
}
function renderLetters() {
  const years = byId("years"); years.replaceChildren();
  atlas.sources.filter(source => source.type === "shareholder_letter")
    .sort((a, b) => a.year - b.year)
    .forEach(source => {
      const link = node("a", "", source.year);
      link.href = source.url; link.target = "_blank"; link.rel = "noopener noreferrer";
      link.title = source.title; link.setAttribute("aria-label", "Read Berkshire " + source.year + " shareholder letter");
      years.append(link);
    });
}
async function start() {
  const input = byId("query");
  const form = byId("search-form");
  form.addEventListener("submit", event => { event.preventDefault(); clearTimeout(inputTimer); setQuery(input.value); });
  input.addEventListener("input", () => { clearTimeout(inputTimer); inputTimer = setTimeout(() => setQuery(input.value), 140); });
  byId("more").addEventListener("click", () => { visible += 10; render(); });
  document.querySelectorAll("[data-example]").forEach(button => button.addEventListener("click", () => {
    input.value = button.dataset.example;
    setQuery(input.value);
    input.focus();
  }));
  document.querySelectorAll("[data-kind]").forEach(button => button.addEventListener("click", () => showKind(button.dataset.kind)));
  document.addEventListener("keydown", event => {
    if (event.key === "/" && !["INPUT", "TEXTAREA"].includes(document.activeElement.tagName) && !event.ctrlKey && !event.metaKey && !event.altKey) {
      event.preventDefault(); input.focus();
    }
  });
  window.addEventListener("popstate", () => {
    input.value = new URLSearchParams(location.search).get("q") || "";
    setQuery(input.value, false);
  });
  input.value = new URLSearchParams(location.search).get("q") || "";
  query = input.value.trim();
  try {
    const response = await fetch("./knowledge/atlas.json");
    if (!response.ok) throw new Error("Source index returned " + response.status);
    const data = await response.json();
    if (data.schemaVersion !== "buffett-brain-atlas-v1" || !Array.isArray(data.entries) || !Array.isArray(data.sources))
      throw new Error("Unexpected source index format");
    atlas = data;
    byId("count-entries").textContent = String(atlas.entries.length);
    byId("count-sources").textContent = String(atlas.sources.length);
    renderLetters();
    render();
  } catch (err) {
    console.error("Source index unavailable", err);
    byId("status").textContent = "The research index could not be loaded. Original case studies and source links remain available above.";
  }
}
start();
