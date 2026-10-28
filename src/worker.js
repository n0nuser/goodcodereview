// Serves site/ as static assets. The Worker runs for paths that match no file, and for the two paths in wrangler.jsonc `run_worker_first`.
// Cloudflare rules, not this Worker, serve index.md for Accept: text/markdown on "/" (see docs/deploy.md).
const MD = "text/markdown; charset=utf-8";
const wantsMarkdown = (req) => /\btext\/markdown\b/i.test(req.headers.get("accept") || "");

const KEYS = { concern: (c) => c.concerns, topic: (c) => c.topics, level: (c) => [c.level] };
const GROUPS = { concern: (c) => c.concerns, topic: (c) => c.topics, level: (c) => [c.level] };
const list = (params, key) => params.getAll(key).flatMap((v) => v.split(",")).map((v) => v.trim().toLowerCase()).filter(Boolean);

// A card matches when, for each of concern, topic, and level that is given, it has any of the given values.
// Values that no card has are reported back and ignored, as the page does.
export function select(corpus, params) {
	const known = { concern: new Set(corpus.concerns), topic: new Set(corpus.cards.flatMap((c) => c.topics)), level: new Set(corpus.levels.map((l) => l.id)) };
	const picked = {}, unknown = [];
	for (const key of Object.keys(KEYS)) {
		const values = list(params, key);
		picked[key] = values.filter((v) => known[key].has(v));
		unknown.push(...values.filter((v) => !known[key].has(v)).map((v) => `${key}=${v}`));
	}
	const cards = corpus.cards.filter((c) => Object.entries(KEYS).every(([key, of]) => !picked[key].length || picked[key].some((v) => of(c).includes(v))));
	return { cards, picked, unknown, known };
}

const line = (c) => `- [\`${c.id}\`](${c.url}) [${c.severity}] {${c.concerns.join(", ")}}: ${c.rule}`;

export function markdown(corpus, params) {
	const { cards, picked, unknown, known } = select(corpus, params);
	const group = params.get("group");
	const picks = Object.entries(picked).filter(([, v]) => v.length).map(([k, v]) => `${k}: ${v.join(", ")}`);
	const out = ["# Concerns", "", picks.length ? `Stable cards that match ${picks.join("; ")}. A card matches when it lists any value given for each filter.` : "All stable cards.",
		`${cards.length} of ${corpus.cards.length} cards.`];
	if (unknown.length) out.push("", `Ignored, not a known value: ${unknown.join(", ")}. Known concerns: ${[...known.concern].join(", ")}. Known levels: ${[...known.level].join(", ")}.`);
	out.push("", "Report each check as `PASS`, `FAIL`, or `N/A` with `file:line` evidence. A `FAIL` carries the card's severity. Any `block` `FAIL` means request changes.");
	if (GROUPS[group]) {
		const keys = group === "concern" ? corpus.concerns : group === "level" ? corpus.levels.map((l) => l.id) : [...known.topic].sort();
		for (const k of keys.filter((k) => !picked[group].length || picked[group].includes(k))) {
			const hit = cards.filter((c) => GROUPS[group](c).includes(k));
			if (hit.length) out.push("", `## ${k}`, "", ...hit.map(line));
		}
		const rest = cards.filter((c) => !GROUPS[group](c).length);
		if (rest.length) out.push("", `## no ${group}`, "", ...rest.map(line));
	} else out.push("", ...cards.map(line));
	return out.join("\n") + "\n";
}

export default {
	async fetch(req, env) {
		const url = new URL(req.url);
		const filtered = ["concern", "topic", "level", "group"].some((k) => url.searchParams.has(k));
		const path = url.pathname;
		const asMarkdown = path === "/concerns.md";
		if (filtered && (asMarkdown || path === "/cards.json") && req.method === "GET") {
			const res = await env.ASSETS.fetch(new Request(new URL("/cards.json", req.url), { headers: { accept: "application/json" } }));
			if (res.ok) {
				const corpus = await res.json();
				const headers = new Headers({ "Cache-Control": "public, max-age=300", "X-Content-Type-Options": "nosniff", Vary: "Accept" });
				if (asMarkdown) {
					headers.set("Content-Type", MD);
					return new Response(markdown(corpus, url.searchParams), { headers });
				}
				headers.set("Content-Type", "application/json; charset=utf-8");
				return new Response(JSON.stringify({ ...corpus, cards: select(corpus, url.searchParams).cards }, null, 1) + "\n", { headers });
			}
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
