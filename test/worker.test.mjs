import test from "node:test";
import assert from "node:assert/strict";
import worker from "../src/worker.js";

// A stand-in for the ASSETS binding: it serves the 404 page and applies one shared header like _headers does.
const files = { "/404.html": ["<h1>missing</h1>", "text/html"] };
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
