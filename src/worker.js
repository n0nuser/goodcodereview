// Serves site/ as static assets. The Worker runs for paths that match no file, and for the two paths in wrangler.jsonc `run_worker_first`.
// A single concern or level is a static file the build writes (cards/concern-<c>.json, cards/<l>.json, concerns/<c>.md, concerns/level-<l>.md);
// agents can fetch those paths directly and skip the Worker. Any other filter is computed here, from cards-index.json (Markdown) or cards.json (JSON).
// Cloudflare rules, not this Worker, serve index.md for Accept: text/markdown on "/" (see docs/deploy.md).
const MD = "text/markdown; charset=utf-8";
const wantsMarkdown = (req) => /\btext\/markdown\b/i.test(req.headers.get("accept") || "");

const KEYS = { concern: (c) => c.concerns, topic: (c) => c.topics, level: (c) => [c.level] };
const GROUPS = KEYS;
const list = (params, key) => params.getAll(key).flatMap((v) => v.split(",")).map((v) => v.trim().toLowerCase()).filter(Boolean);

// A card matches when, for each of concern, topic, and level that is given, it has any of the given values.
// Values that no card has are reported back and ignored, as the page does.
export function select(corpus, params) {
	const known = { concern: new Set(corpus.concerns), topic: new Set(corpus.cards.flatMap((c) => c.topics)), level: new Set(levelIds(corpus)) };
	const picked = {}, unknown = [];
	for (const key of Object.keys(KEYS)) {
		const values = list(params, key);
		picked[key] = values.filter((v) => known[key].has(v));
		unknown.push(...values.filter((v) => !known[key].has(v)).map((v) => `${key}=${v}`));
	}
	// A filter whose values are all unknown matches nothing, so a typo cannot pass for "all cards".
	const given = Object.fromEntries(Object.keys(KEYS).map((key) => [key, list(params, key).length > 0]));
	const cards = corpus.cards.filter((c) => Object.entries(KEYS).every(([key, of]) => !given[key] || picked[key].some((v) => of(c).includes(v))));
	return { cards, picked, unknown, known };
}

// A filter that has its own static file: exactly one value of `key` (concern or level) and no other filter. Returns the value, or "" when the
// request needs the corpus. The value is limited to letters, so it cannot name another path.
const only = (params, key) => {
	const others = ["concern", "topic", "level", "group"].filter((k) => k !== key).some((k) => params.has(k));
	const values = list(params, key);
	return !others && values.length === 1 && /^[a-z]+$/.test(values[0]) ? values[0] : "";
};
export const levelOnly = (params) => only(params, "level");
export const concernOnly = (params) => only(params, "concern");

// cards-index.json lists level ids, cards.json lists level records.
const levelIds = (corpus) => corpus.levels.map((l) => (typeof l === "string" ? l : l.id));

const line = (c) => `- [\`${c.id}\`](${c.url}) [${c.severity}] {${c.concerns.join(", ")}}: ${c.rule}`;

export function markdown(corpus, params) {
	const { cards, picked, unknown, known } = select(corpus, params);
	const group = Object.hasOwn(GROUPS, params.get("group")) ? params.get("group") : "";
	const picks = Object.entries(picked).filter(([, v]) => v.length).map(([k, v]) => `${k}: ${v.join(", ")}`);
	const out = ["# Concerns", "", picks.length ? `Stable cards that match ${picks.join("; ")}. A card matches when it lists any value given for each filter.` : "All stable cards.",
		`${cards.length} of ${corpus.cards.length} cards.`];
	if (unknown.length) out.push("", `Ignored, not a known value: ${unknown.join(", ")}. Known concerns: ${[...known.concern].join(", ")}. Known levels: ${[...known.level].join(", ")}.`);
	out.push("", "Report each check as `PASS`, `FAIL`, or `N/A` with `file:line` evidence. A `FAIL` carries the card's severity. Any `block` `FAIL` means request changes.");
	if (group) {
		const keys = group === "concern" ? corpus.concerns : group === "level" ? levelIds(corpus) : [...known.topic].sort();
		for (const k of keys.filter((k) => !picked[group].length || picked[group].includes(k))) {
			const hit = cards.filter((c) => GROUPS[group](c).includes(k));
			if (hit.length) out.push("", `## ${k}`, "", ...hit.map(line));
		}
		const rest = cards.filter((c) => !GROUPS[group](c).length);
		if (rest.length) out.push("", `## no ${group}`, "", ...rest.map(line));
	} else out.push("", ...cards.map(line));
	return out.join("\n") + "\n";
}

const headersFor = (type) => new Headers({ "Cache-Control": "public, max-age=300", "X-Content-Type-Options": "nosniff", Vary: "Accept", "Content-Type": type });
const JSON_TYPE = "application/json; charset=utf-8";

// The static file for a single concern or level, served as is: no parse, no filter. The build writes these files.
const STATIC = {
	"/cards.json": { type: JSON_TYPE, concern: (v) => `/cards/concern-${v}.json`, level: (v) => `/cards/${v}.json` },
	"/concerns.md": { type: MD, concern: (v) => `/concerns/${v}.md`, level: (v) => `/concerns/level-${v}.md` },
};

async function staticFile(req, env, url) {
	const route = STATIC[url.pathname];
	const hit = route && [["concern", concernOnly(url.searchParams)], ["level", levelOnly(url.searchParams)]].find(([, v]) => v);
	if (!hit) return null;
	const file = await env.ASSETS.fetch(new Request(new URL(route[hit[0]](hit[1]), req.url), { headers: { accept: route.type } }));
	return file.ok ? new Response(req.method === "HEAD" ? null : file.body, { headers: headersFor(route.type) }) : null;
}

// Filters that need the corpus. Markdown reads the slim index (it uses only the slim fields); JSON needs the full cards.
async function filtered(req, env, url) {
	const asMarkdown = url.pathname === "/concerns.md";
	const res = await env.ASSETS.fetch(new Request(new URL(asMarkdown ? "/cards-index.json" : "/cards.json", req.url), { headers: { accept: "application/json" } }));
	if (!res.ok) return null;
	const corpus = await res.json();
	const head = req.method === "HEAD";
	if (asMarkdown) return new Response(head ? null : markdown(corpus, url.searchParams), { headers: headersFor(MD) });
	return new Response(head ? null : JSON.stringify({ ...corpus, cards: select(corpus, url.searchParams).cards }, null, 1) + "\n", { headers: headersFor(JSON_TYPE) });
}

// A GET answer is kept in the Cache API under the request URL, so the same filter costs no second parse. Cache-Control on the response sets its lifetime.
async function cached(req, ctx, build) {
	const cache = globalThis.caches?.default;
	if (!cache || req.method !== "GET") return build();
	const key = new Request(req.url);
	const hit = await cache.match(key);
	if (hit) return hit;
	const res = await build();
	if (res) ctx?.waitUntil(cache.put(key, res.clone()));
	return res;
}

export default {
	async fetch(req, env, ctx) {
		const url = new URL(req.url);
		const readOnly = req.method === "GET" || req.method === "HEAD";
		const wantsFilter = ["concern", "topic", "level", "group"].some((k) => url.searchParams.has(k));
		if (readOnly && (url.pathname === "/concerns.md" || url.pathname === "/cards.json") && wantsFilter) {
			const res = (await staticFile(req, env, url)) ?? (await cached(req, ctx, () => filtered(req, env, url)));
			if (res) return res;
		}
		const asset = await env.ASSETS.fetch(req);
		if (asset.status !== 404) return asset;
		const page = await env.ASSETS.fetch(new Request(new URL("/404.html", req.url), { headers: req.headers }));
		if (!wantsMarkdown(req)) return new Response(page.body, { status: 404, headers: page.headers });
		const headers = new Headers(page.headers);
		headers.set("Content-Type", MD);
		headers.delete("Content-Length");
		headers.append("Vary", "Accept");
		return new Response(
			"# Not found\n\nNo page exists at this path. Start from the [site index](/llms.txt) or the [sitemap](/sitemap.xml).\n",
			{ status: 404, headers },
		);
	},
};
