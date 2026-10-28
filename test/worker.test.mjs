import test from "node:test";
import assert from "node:assert/strict";
import worker from "../src/worker.js";

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
const files = { "/404.html": ["<h1>missing</h1>", "text/html"], "/cards.json": [JSON.stringify(corpus), "application/json"], "/concerns.md": ["static", "text/markdown"] };
const env = {
	ASSETS: {
		async fetch(req) {
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
