import test from "node:test";
import { createHash } from "node:crypto";
import { readFileSync, readdirSync, existsSync } from "node:fs";
import assert from "node:assert/strict";
import worker, { concernOnly, levelOnly, markdown } from "../src/worker.js";

// A stand-in for the ASSETS binding: it serves the 404 page and applies one shared header like _headers does.
const corpus = {
	concerns: ["security", "performance", "usability"],
	levels: [{ id: "change" }, { id: "function" }],
	cards: [
		{ id: "a", level: "function", severity: "block", concerns: ["security"], topics: ["injection"], rule: "Bind parameters.", url: "https://x/function#a" },
		{ id: "b", level: "function", severity: "should-fix", concerns: ["performance"], topics: ["io"], rule: "Batch.", url: "https://x/function#b" },
		{ id: "c", level: "change", severity: "discuss", concerns: ["security", "usability"], topics: [], rule: "Small.", url: "https://x/change#c" },
	],
};
const index = { ...corpus, levels: corpus.levels.map((l) => l.id) };
const files = { "/cards-index.json": [JSON.stringify(index), "application/json"],
	"/cards/concern-security.json": ['{"concern-file":"security"}', "application/json"],
	"/concerns/security.md": ["# security file", "text/markdown"], "/concerns/level-function.md": ["# function file", "text/markdown"],
	"/404.html": ["<h1>missing</h1>", "text/html"], "/cards.json": [JSON.stringify(corpus), "application/json"], "/concerns.md": ["static", "text/markdown"],
	"/cards/function.json": ['{"level-file":"function"}', "application/json"] };
const seen = [];
const env = {
	ASSETS: {
		async fetch(req) {
			seen.push(new URL(req.url).pathname);
			const hit = files[new URL(req.url).pathname];
			if (!hit) return new Response("no", { status: 404 });
			return new Response(hit[0], { headers: { "Content-Type": hit[1], "X-Content-Type-Options": "nosniff" } });
		},
	},
};
const get = (path, accept) => worker.fetch(new Request("https://example.com" + path, accept ? { headers: { Accept: accept } } : {}), env);

test("an unknown path returns the HTML 404 page", async () => {
	const res = await get("/nope");
	assert.equal(res.status, 404);
	assert.equal(await res.text(), "<h1>missing</h1>");
});

test("an unknown path returns a Markdown 404 with a link to llms.txt", async () => {
	const res = await get("/nope", "text/markdown");
	assert.equal(res.status, 404);
	assert.equal(res.headers.get("content-type"), "text/markdown; charset=utf-8");
	assert.equal(res.headers.get("x-content-type-options"), "nosniff");
	assert.match(await res.text(), /\(\/llms\.txt\)/);
});

test("concerns.md with no filter is served as the static file", async () => {
	assert.equal(await (await get("/concerns.md")).text(), "static");
});

test("concerns.md filters by concern, topic, and level; any value in one filter matches", async () => {
	const all = await (await get("/concerns.md?concern=security,performance")).text();
	assert.match(all, /2 of 3|3 of 3/);
	const body = await (await get("/concerns.md?concern=security&level=function")).text();
	assert.match(body, /`a`/);
	assert.doesNotMatch(body, /`b`|`c`/);
	const topic = await (await get("/concerns.md?topic=io&topic=injection")).text();
	assert.match(topic, /`a`[\s\S]*`b`/);
	assert.doesNotMatch(topic, /`c`/);
});

test("concerns.md reports unknown values and groups on request", async () => {
	const body = await (await get("/concerns.md?concern=nope,usability&group=concern")).text();
	assert.match(body, /Ignored, not a known value: concern=nope/);
	assert.match(body, /## usability\n\n- \[`c`\]/);
	assert.doesNotMatch(body, /## security/);
});

test("cards.json filters to the matching cards and keeps the corpus fields", async () => {
	const res = await get("/cards.json?level=change");
	assert.equal(res.headers.get("content-type"), "application/json; charset=utf-8");
	const data = await res.json();
	assert.deepEqual(data.cards.map((c) => c.id), ["c"]);
	assert.deepEqual(data.concerns, corpus.concerns);
	assert.equal((await (await get("/cards.json")).json()).cards.length, 3);
});

test("a group name that is an Object.prototype key is ignored, not a 500", async () => {
	for (const g of ["constructor", "toString", "__proto__"]) {
		const res = await get(`/concerns.md?group=${g}`);
		assert.equal(res.status, 200, g);
		assert.match(await res.text(), /`a`/);
	}
});

test("a filter with only unknown values matches nothing", async () => {
	const data = await (await get("/cards.json?concern=securty")).json();
	assert.deepEqual(data.cards, []);
	assert.match(await (await get("/concerns.md?concern=securty")).text(), /0 of 3 cards[\s\S]*Ignored/);
});

test("HEAD gets the filtered headers and no body", async () => {
	const res = await worker.fetch(new Request("https://example.com/cards.json?level=change", { method: "HEAD" }), env);
	assert.equal(res.headers.get("cache-control"), "public, max-age=300");
	assert.equal(await res.text(), "");
});

test("a single level is served from its own file without reading the corpus", async () => {
	seen.length = 0;
	const res = await get("/cards.json?level=function");
	assert.equal(res.headers.get("content-type"), "application/json; charset=utf-8");
	assert.equal(res.headers.get("cache-control"), "public, max-age=300");
	assert.equal(res.headers.get("x-content-type-options"), "nosniff");
	assert.equal(await res.text(), '{"level-file":"function"}');
	assert.deepEqual(seen, ["/cards/function.json"]);
});

test("HEAD on the level file has headers and no body", async () => {
	const res = await worker.fetch(new Request("https://example.com/cards.json?level=function", { method: "HEAD" }), env);
	assert.equal(res.headers.get("content-type"), "application/json; charset=utf-8");
	assert.equal(await res.text(), "");
});

test("a level with no file falls back to filtering the corpus", async () => {
	const data = await (await get("/cards.json?level=change")).json();
	assert.deepEqual(data.cards.map((c) => c.id), ["c"]);
	const none = await (await get("/cards.json?level=nope")).json();
	assert.deepEqual(none.cards, []);
});

test("level plus another filter, several levels, or a path-like value use the corpus", async () => {
	for (const q of ["level=function&concern=security", "level=function&group=level", "level=function&topic=io", "level=function,change", "level=function&level=change", "level=..%2Fx", "level=Function%2F"]) {
		seen.length = 0;
		const data = await (await get(`/cards.json?${q}`)).json();
		assert.ok(Array.isArray(data.cards), q);
		assert.ok(seen.includes("/cards.json"), q);
		assert.ok(!seen.some((p) => p.startsWith("/cards/")), q);
	}
	assert.deepEqual((await (await get("/cards.json?level=function&concern=security")).json()).cards.map((c) => c.id), ["a"]);
});

test("levelOnly accepts one letters-only level and nothing else", () => {
	const p = (q) => new URLSearchParams(q);
	assert.equal(levelOnly(p("level=Function")), "function");
	assert.equal(levelOnly(p("level=function&concern=security")), "");
	assert.equal(levelOnly(p("level=function,change")), "");
	assert.equal(levelOnly(p("level=a/b")), "");
	assert.equal(levelOnly(p("")), "");
});

test("an unfiltered cards.json is passed through to the static file", async () => {
	seen.length = 0;
	assert.equal((await (await get("/cards.json")).json()).cards.length, 3);
	assert.deepEqual(seen, ["/cards.json"]);
});

// --- static routes, golden output, and the Cache API ---

const sha = (text) => createHash("sha256").update(text).digest("hex");
const siteDir = new URL("../site/", import.meta.url);
const built = existsSync(new URL("cards-index.json", siteDir));
// An ASSETS binding backed by the built site/, for the tests that compare against real output.
const builtEnv = {
	ASSETS: {
		async fetch(req) {
			const file = new URL("." + new URL(req.url).pathname, siteDir);
			return existsSync(file) && !file.pathname.endsWith("/") ? new Response(readFileSync(file), { headers: { "Content-Type": "application/octet-stream" } }) : new Response("no", { status: 404 });
		},
	},
};
const builtGet = (path) => worker.fetch(new Request("https://example.com" + path), builtEnv);

test("a single concern is served from its own file without reading the corpus", async () => {
	for (const [path, body, type] of [["/cards.json?concern=security", '{"concern-file":"security"}', "application/json; charset=utf-8"], ["/concerns.md?concern=security", "# security file", "text/markdown; charset=utf-8"]]) {
		seen.length = 0;
		const res = await get(path);
		assert.equal(await res.text(), body, path);
		assert.equal(res.headers.get("content-type"), type, path);
		assert.equal(res.headers.get("cache-control"), "public, max-age=300", path);
		assert.equal(seen.length, 1, path);
	}
});

test("a single level in Markdown is served from its own file", async () => {
	assert.equal(await (await get("/concerns.md?level=function")).text(), "# function file");
});

test("HEAD on a concern file has headers and no body", async () => {
	const res = await worker.fetch(new Request("https://example.com/concerns.md?concern=security", { method: "HEAD" }), env);
	assert.equal(res.headers.get("content-type"), "text/markdown; charset=utf-8");
	assert.equal(await res.text(), "");
});

test("a concern with no file, or with another filter, is computed from the corpus", async () => {
	seen.length = 0;
	const body = await (await get("/concerns.md?concern=usability")).text();
	assert.match(body, /Stable cards that match concern: usability/);
	assert.deepEqual(seen, ["/concerns/usability.md", "/cards-index.json"]); // the missing static file, then the slim index
	seen.length = 0;
	const json = await (await get("/cards.json?concern=usability")).json();
	assert.deepEqual(json.cards.map((c) => c.id), ["c"]);
	assert.deepEqual(seen, ["/cards/concern-usability.json", "/cards.json"]); // the missing static file, then the full corpus
	for (const q of ["concern=security&level=function", "concern=security,usability", "concern=security&group=level", "concern=security&topic=io"]) {
		assert.doesNotMatch(await (await get(`/concerns.md?${q}`)).text(), /security file/, q);
	}
});

test("concernOnly accepts one letters-only concern and nothing else", () => {
	const p = (q) => new URLSearchParams(q);
	assert.equal(concernOnly(p("concern=Security")), "security");
	assert.equal(concernOnly(p("concern=security&level=function")), "");
	assert.equal(concernOnly(p("concern=security,usability")), "");
	assert.equal(concernOnly(p("concern=../x")), "");
	assert.equal(concernOnly(p("level=function")), "");
});

test("Markdown output is unchanged from the captured golden hashes", { skip: !built && "run python3 tools/build.py first" }, async () => {
	const golden = JSON.parse(readFileSync(new URL("./golden/concerns-md.json", import.meta.url), "utf8")).queries;
	const queries = Object.entries(golden);
	assert.ok(queries.length >= 20);
	for (const [q, want] of queries) {
		const text = await (await builtGet(`/concerns.md${q ? "?" + q : ""}`)).text();
		assert.deepEqual({ sha256: sha(text), length: Buffer.byteLength(text) }, want, q || "(no filter)");
	}
});

test("every static concern and level Markdown file equals the Worker's own output", { skip: !built && "run python3 tools/build.py first" }, () => {
	const index = JSON.parse(readFileSync(new URL("cards-index.json", siteDir), "utf8"));
	const names = readdirSync(new URL("concerns/", siteDir));
	assert.ok(names.length >= 10);
	for (const name of names) {
		const stem = name.replace(/\.md$/, "");
		const params = new URLSearchParams(stem.startsWith("level-") ? { level: stem.slice(6) } : { concern: stem });
		assert.equal(readFileSync(new URL(`concerns/${name}`, siteDir), "utf8"), markdown(index, params), name);
	}
});

test("static concern JSON files hold the cards that list the concern", { skip: !built && "run python3 tools/build.py first" }, () => {
	const all = JSON.parse(readFileSync(new URL("cards.json", siteDir), "utf8"));
	for (const concern of all.concerns) {
		const file = new URL(`cards/concern-${concern}.json`, siteDir);
		if (!existsSync(file)) continue;
		const part = JSON.parse(readFileSync(file, "utf8"));
		assert.deepEqual(part.cards.map((c) => c.id), all.cards.filter((c) => c.concerns.includes(concern)).map((c) => c.id), concern);
	}
});

// A fake Cache API: it records puts and returns what it holds for a URL.
function withCache(fn) {
	const store = new Map(), puts = [], matches = [];
	globalThis.caches = {
		default: {
			async match(key) { matches.push(key.url); return store.get(key.url)?.clone(); },
			async put(key, res) { puts.push(key.url); store.set(key.url, res); },
		},
	};
	const waits = [];
	const ctx = { waitUntil: (p) => waits.push(p) };
	return fn({ store, puts, matches, ctx, settle: () => Promise.all(waits) }).finally(() => delete globalThis.caches);
}
const getWith = (path, ctx, method = "GET") => worker.fetch(new Request("https://example.com" + path, { method }), env, ctx);

test("a computed answer is cached by URL and the second request reads the cache", () => withCache(async ({ puts, matches, ctx, settle }) => {
	seen.length = 0;
	const first = await getWith("/concerns.md?concern=usability&level=change", ctx);
	await settle();
	assert.deepEqual(puts, ["https://example.com/concerns.md?concern=usability&level=change"]);
	assert.equal(first.headers.get("cache-control"), "public, max-age=300");
	const reads = seen.length;
	const second = await getWith("/concerns.md?concern=usability&level=change", ctx);
	assert.equal(await second.text(), await first.text());
	assert.equal(seen.length, reads);
	assert.equal(matches.length, 2);
	assert.equal(puts.length, 1);
}));

test("static files, HEAD, other paths, and misses are not cached", () => withCache(async ({ puts, ctx, settle }) => {
	await getWith("/concerns.md?concern=security", ctx);
	await getWith("/cards.json?level=function", ctx);
	await getWith("/concerns.md?concern=usability&level=change", ctx, "HEAD");
	await getWith("/nope", ctx);
	await settle();
	assert.deepEqual(puts, []);
}));

test("without a Cache API the answer is computed as before", async () => {
	const res = await getWith("/concerns.md?concern=usability&level=change", undefined);
	assert.match(await res.text(), /usability/);
});
