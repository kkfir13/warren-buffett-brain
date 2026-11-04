import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { coverage, searchEvidence, recordById } from "./evidence.mjs";

const atlas = JSON.parse(readFileSync(new URL("../knowledge/atlas.json", import.meta.url), "utf8"));

test("expected canonical research corpus is loaded", () => {
  assert.equal(atlas.sources.length, 60);
  assert.equal(atlas.entries.length, 55);
  assert.equal(coverage(atlas).originalResearchNotes, 55);
});

test("search finds source-linked historical records", () => {
  const r = searchEvidence(atlas, "GEICO");
  assert.ok(r.total > 0);
  assert.ok(r.results.length <= 5);
  assert.ok(r.results.some(x => x.title.toLowerCase().includes("geico") || x.snippet.toLowerCase().includes("geico")));
  assert.ok(r.results.every(x => x.sources.every(s => s.url.startsWith("https://"))));
});

test("search limit is bounded; empty or invalid query is safe", () => {
  assert.equal(searchEvidence(atlas, "").total, 0);
  assert.ok(searchEvidence(atlas, "buffett", 9999).results.length <= 10);
  assert.equal(searchEvidence(atlas, "zzzxxyyqqq").total, 0);
});

test("fetched notes contain real original publisher links and limitations", () => {
  const match = searchEvidence(atlas, "Dexter Shoe", 1).results[0];
  assert.ok(match);
  const detail = recordById(atlas, match.id);
  assert.equal(detail.recordType, "research-note");
  assert.ok(detail.summary && detail.evidence);
  assert.ok(Array.isArray(detail.sourceLinks));
  assert.ok(detail.sourceLinks.length > 0);
  assert.ok(detail.sourceLinks.every(s => /^https:\/\//.test(s.url)));
});

test("only existing IDs can be retrieved", () => {
  assert.equal(recordById(atlas, "arbitrary-url-https://example.com"), null);
  assert.equal(recordById(atlas, ""), null);
  assert.equal(recordById(atlas, "../../private-data"), null);
});

test("source lookup clearly labels source as link only", () => {
  const s = recordById(atlas, "letter-1989");
  assert.equal(s.recordType, "source");
  assert.match(s.note, /not proof/);
});
