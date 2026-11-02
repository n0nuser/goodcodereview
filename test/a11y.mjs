// Runs axe-core on built pages in jsdom and exits 1 on any violation. Run `python3 tools/build.py` first.
// jsdom does no layout, so the colour-contrast rule is off; the CSS palette is checked by hand against WCAG 2.2.
//   node test/a11y.mjs [page.html ...]     default: index.html function.html concerns.html
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import axe from "axe-core";
import { JSDOM } from "jsdom";

const SITE = fileURLToPath(new URL("../site/", import.meta.url));
const DEFAULT_PAGES = ["index.html", "function.html", "concerns.html"];
const RULES = { "color-contrast": { enabled: false } };

export async function check(file) {
	const dom = new JSDOM(readFileSync(SITE + file, "utf8"), { runScripts: "outside-only", pretendToBeVisual: true });
	dom.window.eval(axe.source);
	const { violations, passes } = await dom.window.axe.run(dom.window.document, { rules: RULES, resultTypes: ["violations", "passes"] });
	dom.window.close();
	return { file, violations, passes: passes.length };
}

const pages = process.argv.length > 2 ? process.argv.slice(2) : DEFAULT_PAGES;
let failed = 0;
for (const file of pages) {
	const { violations, passes } = await check(file);
	console.log(`${violations.length ? "FAIL" : "PASS"}  ${file}: ${violations.length} violation(s), ${passes} rule(s) passed`);
	for (const v of violations) {
		failed += v.nodes.length;
		console.log(`  ${v.id} (${v.impact}): ${v.help}\n    ${v.helpUrl}`);
		for (const n of v.nodes.slice(0, 3)) console.log(`    ${n.target.join(" ")}`);
	}
}
process.exit(failed ? 1 : 0);
