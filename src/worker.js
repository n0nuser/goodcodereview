// Serves site/ as static assets. The Worker runs only for paths that match no file, and answers them with a 404.
// Cloudflare rules, not this Worker, serve index.md for Accept: text/markdown on "/" (see docs/deploy.md).
const MD = "text/markdown; charset=utf-8";
const wantsMarkdown = (req) => /\btext\/markdown\b/i.test(req.headers.get("accept") || "");

export default {
	async fetch(req, env) {
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
