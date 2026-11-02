// The page script registers read-only WebMCP tools when document.modelContext exists, and does nothing when it does not.
//   node --test test/webmcp.test.mjs     (run `python3 tools/build.py` first)
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import { fileURLToPath } from "node:url";
import { JSDOM } from "jsdom";

const SITE = fileURLToPath(new URL("../site/", import.meta.url));
async function run(file, withApi = true) {
	const tools = new Map();
	const html = readFileSync(SITE + file, "utf8");
	const dom = new JSDOM(html, {
		url: "https://goodcodereview.com/" + file, runScripts: "dangerously",
		beforeParse(w) { w.matchMedia = () => ({ matches: false }); if (withApi) w.document.modelContext = { registerTool: async (t) => { tools.set(t.name, t); } }; },
	});
	await new Promise((r) => setTimeout(r, 20));
	return { tools, dom };
}

test("home registers start_review and list_levels", async () => {
	const { tools } = await run("index.html");
	assert.deepEqual([...tools.keys()].sort(), ["list_levels", "start_review"]);
	const levels = JSON.parse(await tools.get("list_levels").execute({}));
	assert.equal(levels.length, 8);
	assert.match(JSON.parse(await tools.get("start_review").execute({})).prompt, /llms\.txt/);
	assert.equal(tools.get("start_review").annotations.readOnlyHint, true);
});

test("a level page also registers list_cards, filtered by concern", async () => {
	const { tools } = await run("function.html");
	const all = JSON.parse(await tools.get("list_cards").execute({}));
	const sec = JSON.parse(await tools.get("list_cards").execute({ concern: "security" }));
	assert.ok(all.length > 0 && sec.length > 0 && sec.length < all.length);
	assert.deepEqual(Object.keys(all[0]).sort(), ["id", "rule", "severity", "url"]);
});

test("without the API the page still works", async () => {
	const { tools, dom } = await run("function.html", false);
	assert.equal(tools.size, 0);
	assert.ok(dom.window.document.querySelector("#flat"));
});
