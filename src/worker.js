// Serves site/ as static assets. The Worker runs only for "/" and for paths that match no asset.
// "/" answers Accept: text/markdown with the Markdown twin. Unknown paths answer 404 in HTML or Markdown.
const MD = "text/markdown; charset=utf-8";
const wantsMarkdown = (req) => /\btext\/markdown\b/i.test(req.headers.get("accept") || "");

async function asset(env, req, path) {
	return env.ASSETS.fetch(new Request(new URL(path, req.url), { headers: req.headers }));
}

export default {
	async fetch(req, env) {
		const { pathname } = new URL(req.url);
		if (pathname === "/") {
			const res = wantsMarkdown(req) ? await asset(env, req, "/index.md") : await env.ASSETS.fetch(req);
			const out = new Response(res.body, res);
			if (wantsMarkdown(req)) out.headers.set("Content-Type", MD);
			out.headers.append("Vary", "Accept");
			return out;
		}
		const page = await asset(env, req, "/404.html");
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
