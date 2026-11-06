"""Static assets inlined into every page: CSS, JavaScript, and the favicon."""
import json

from models import LEVELS

CSS = """*,*::before,*::after{box-sizing:border-box;min-width:0}
:root{color-scheme:light dark;
--bg:light-dark(oklch(.985 0 none),oklch(.18 0 none));--fg:light-dark(oklch(.2 0 none),oklch(.93 0 none));
--mut:light-dark(oklch(.45 0 none),oklch(.76 0 none));--line:light-dark(oklch(.88 0 none),oklch(.32 0 none));
--edge:light-dark(oklch(.58 0 none),oklch(.58 0 none));
--acc:light-dark(oklch(.45 .09 190),oklch(.8 .08 180));--bad:light-dark(oklch(.48 .17 27),oklch(.78 .13 25));
--warn:light-dark(oklch(.47 .1 70),oklch(.8 .12 80));--good:light-dark(oklch(.45 .11 150),oklch(.78 .12 150));
--code:color-mix(in oklch,var(--fg) 6%,var(--bg));
--text:Charter,"Bitstream Charter","Sitka Text",Cambria,"Iowan Old Style","Palatino Linotype","Noto Serif",serif;
--ui:Seravek,"Gill Sans Nova",Ubuntu,Calibri,"DejaVu Sans","Noto Sans",sans-serif;
--mono:ui-monospace,"Cascadia Code","SF Mono",Menlo,Consolas,"DejaVu Sans Mono",monospace;
--narrow:20;--wide:77.5;--size-narrow:1;--size-wide:1.125;--ratio-narrow:1.2;--ratio-wide:1.25;
--fluid:clamp(0rem,(100vw - var(--narrow)*1rem)/(var(--wide) - var(--narrow)),1rem);
--at-narrow:calc(var(--size-narrow)*(1rem - var(--fluid)));--at-wide:calc(var(--size-wide)*var(--fluid));
--step-0:calc(var(--at-narrow) + var(--at-wide));--step--1:calc(var(--step-0)/var(--ratio-narrow));
--step-1:calc(var(--at-narrow)*var(--ratio-narrow) + var(--at-wide)*var(--ratio-wide));
--step-3:calc(var(--at-narrow)*pow(var(--ratio-narrow),3) + var(--at-wide)*pow(var(--ratio-wide),3));
--space-s:var(--step-0);--space-m:calc(1.5*var(--step-0));--space-l:calc(2*var(--step-0));--gutter:clamp(1rem,4vw,2rem);
--ease-out:cubic-bezier(.23,1,.32,1);
scrollbar-gutter:stable;scroll-padding-block-start:var(--space-m);text-wrap:pretty;overflow-wrap:break-word;font-synthesis:none;
-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;-webkit-text-size-adjust:100%;-webkit-tap-highlight-color:transparent}
[hidden]{display:none!important}
h1,h2,h3,h4{text-wrap:balance}
input,textarea,select{font-size:max(16px,1rem)}
button,a,summary{touch-action:manipulation}button{user-select:none;-webkit-user-select:none}
body{margin:0;min-block-size:100svh;display:grid;grid-template-rows:auto 1fr auto;align-content:start;
grid-template-columns:minmax(var(--gutter),1fr) minmax(0,62rem) minmax(var(--gutter),1fr);
background:var(--bg);color:var(--fg);font:var(--step-0)/1.55 var(--text)}
body>*{grid-column:2}
:where(h1,h2,h3,p,ul,pre,figure){margin:0}
:is(main,article)>*+*{margin-block-start:var(--space-s)}
p{max-inline-size:68ch}ul:not([class]){padding-inline-start:1.25em;max-inline-size:68ch}
h1,h2,h3{font-family:var(--ui);line-height:1.2}
main>h1{margin-block-start:var(--space-l);font-size:var(--step-3);font-weight:700;letter-spacing:-.01em}
main>h2{margin-block-start:var(--space-l);padding-block-start:var(--space-s);border-block-start:2px solid var(--fg);font-size:var(--step-1)}
article>h2{font-size:var(--step-1)}
h3{font:600 var(--step-0)/1.2 var(--mono)}
a{color:var(--acc);text-decoration-thickness:.07em;text-underline-offset:.2em}
:focus-visible{outline:max(2px,.08em) solid var(--acc);outline-offset:.2em}
nav{display:flex;flex-wrap:wrap;align-items:center;gap:0 var(--space-m);padding-block:var(--space-s);border-block-end:1px solid var(--line);font:var(--step--1)/1.3 var(--ui)}
nav a,nav summary{display:flex;align-items:center;min-block-size:44px;padding-block:0;color:var(--fg);text-decoration:none}
nav a[aria-current]{font-weight:700;text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:.35em}
nav{position:relative}nav>a{position:relative;z-index:12}nav>a:last-child{margin-inline-start:auto}
nav details{position:relative;border:0}nav details>summary{gap:.4em;list-style:none;cursor:pointer;border:0}nav summary::-webkit-details-marker{display:none}
nav summary::after{content:"";inline-size:.38em;block-size:.38em;margin-block-start:-.2em;border:solid currentColor;border-width:0 1.5px 1.5px 0;transform:rotate(45deg);transition:transform .15s}
nav details[open]>summary::after{margin-block-start:.2em;transform:rotate(225deg)}
nav details[open]>summary::before{content:"";position:fixed;inset:0;z-index:10;cursor:default}
nav details:has([aria-current])>summary{font-weight:700}
nav{column-gap:var(--space-s)}@media(min-width:34em){nav{column-gap:var(--space-m)}}
nav.crumbs{display:block;padding:0;border:0}.crumbs ol{display:flex;flex-wrap:wrap;gap:0 var(--space-s);margin:0;padding:0;list-style:none}.crumbs li{display:flex;align-items:center;min-block-size:44px}.crumbs li+li::before{content:"/";margin-inline-end:var(--space-s);color:var(--mut)}
nav details>div{position:absolute;inset-block-start:calc(100% - .25rem);inset-inline-start:-.75rem;z-index:20;display:flex;flex-direction:column;min-inline-size:13rem;padding:.35rem;background:var(--bg);border:1px solid var(--line);border-radius:.5rem;box-shadow:0 .5rem 1.5rem light-dark(oklch(0 0 0/.12),oklch(0 0 0/.5))}
nav details>div a{min-block-size:40px;padding-inline:.75rem;border-radius:.35rem;white-space:nowrap}
@media(max-width:34em){nav details{position:static}nav details>div{inset-inline:0;min-inline-size:0}nav details>div a{white-space:normal}}
.skip{position:absolute;inset-block-start:-100px;inset-inline-start:var(--space-s);z-index:1;display:flex;align-items:center;min-block-size:44px;padding-inline:var(--space-s);background:var(--bg);color:var(--fg);border:2px solid var(--acc);font:600 var(--step--1)/1.3 var(--ui)}
.skip:focus{inset-block-start:var(--space-s)}
.vh{position:absolute;inline-size:1px;block-size:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
main:focus{outline:none}
code{font:.9em var(--mono);padding:.08em .3em;background:var(--code);border-radius:2px;overflow-wrap:anywhere}
pre{padding:var(--space-s);overflow-x:auto;background:var(--code);border-radius:2px;font:var(--step--1)/1.5 var(--mono);tab-size:4}
pre code{padding:0;background:none;font:inherit;overflow-wrap:normal}
pre.wrap{max-inline-size:68ch;white-space:pre-wrap;overflow-wrap:anywhere}pre.wrap code{overflow-wrap:anywhere}
.b{display:inline-block;padding:.05em .45em;border:1px solid currentColor;border-radius:2px;color:var(--mut);font:600 var(--step--1)/1.3 var(--ui);white-space:nowrap}
.block{color:var(--bad)}.should-fix{color:var(--warn)}.ok{color:var(--good)}pre .block,pre .should-fix,pre .ok{font-weight:700}.stable{color:var(--fg)}.draft{border-style:dashed}
.tags{display:flex;flex-wrap:wrap;gap:0 .7em;color:var(--mut);font:var(--step--1)/1.4 var(--ui)}
.note{color:var(--mut);font:var(--step--1)/1.5 var(--ui)}
.by{color:var(--mut);font:var(--step--1)/1.5 var(--ui)}.by .note{margin:0}
.orgs{list-style:none;margin:0;padding:0}.orgs li{padding-inline-start:1.9em;text-indent:-1.9em}
.orgs .oi{inline-size:1.25em;block-size:1.25em;vertical-align:-.3em;margin-inline-end:.5em;color:var(--fg)}.on{color:var(--fg);font-weight:600}
.orgs a{display:inline-block;min-block-size:24px;line-height:24px;text-indent:0;overflow-wrap:anywhere}
.sprite{position:absolute;inline-size:0;block-size:0;overflow:hidden}
.legend{display:grid;grid-template-columns:max-content 1fr;gap:.4rem var(--space-s);padding:0;list-style:none;font:var(--step--1)/1.4 var(--ui)}
.legend li{grid-column:1/-1;display:grid;grid-template-columns:subgrid;align-items:baseline}.legend .b{justify-self:start}.legend li.tg{display:block}
.flt{display:flex;flex-wrap:wrap;align-items:center;gap:.75rem .5rem}
.n{font-weight:400;opacity:.8;font-variant-numeric:tabular-nums}button[aria-pressed=true] .n{opacity:1}
select{padding:.4rem .5rem;color:var(--fg);background:var(--bg);border:1px solid var(--edge);border-radius:3px;font:500 var(--step--1)/1.2 var(--ui);min-block-size:44px}
#clr{min-block-size:44px}
h3.gh{margin-block:var(--space-m) .25rem;font:700 var(--step-0)/1.2 var(--ui);text-transform:capitalize}
details.fg>summary{font-weight:600}.sel{color:var(--mut);font-weight:400}details.fg>.flt{padding-block:.25rem .75rem}
.lab{flex:none;inline-size:6.5rem;color:var(--mut);font:600 var(--step--1)/1.3 var(--ui)}
button{position:relative;padding:.4rem .7rem;color:var(--fg);background:none;border:1px solid var(--edge);border-radius:3px;font:500 var(--step--1)/1.2 var(--ui);cursor:pointer;transition:background-color .15s,border-color .15s}
button::after{content:"";position:absolute;inset:min(0px,(100% - 44px)/2)}
button[aria-pressed=true]{font-weight:700;background:var(--acc);border-color:var(--acc);color:var(--bg)}
button:active{transform:scale(.97)}
details{border-block-start:1px solid var(--line)}
summary{padding-block:.75rem;cursor:pointer;font:600 var(--step--1)/1.3 var(--ui)}
details[open]>summary{border-block-end:1px solid var(--line)}
#dsum,#empty,#count{font-variant-numeric:tabular-nums}
.ckw{container-type:inline-size}
ul.ck{padding:0;list-style:none}
ul.ck li{display:flex;flex-wrap:wrap;align-items:baseline;gap:.2rem var(--space-s);padding-block:.6rem;border-block-start:1px solid var(--line)}
ul.ck a{font:600 var(--step--1)/1.4 var(--mono)}
ul.ck .r{flex:1 0 100%;max-inline-size:68ch}
ul.ck .th{display:none}
@container (min-width:46rem){
ul.ck{display:grid;grid-template-columns:max-content max-content fit-content(11rem) minmax(0,1fr);column-gap:var(--space-m)}
ul.ck li{grid-column:1/-1;display:grid;grid-template-columns:subgrid}
ul.ck .r{flex:none}
ul.ck .th{display:grid;border-block-start:0;border-block-end:1px solid var(--edge);padding-block:.25rem;color:var(--mut);font:600 var(--step--1)/1.3 var(--ui)}
}
ul.idx{padding:0;list-style:none}
ul.idx li{display:flex;flex-wrap:wrap;gap:0 var(--space-s);padding-block:.55rem;border-block-start:1px solid var(--line)}
ul.idx a{flex:1 1 10rem;font:600 var(--step-0)/1.5 var(--ui)}ul.idx span{flex:3 1 22rem}ul.idx span.n{flex:1 1 10rem;color:var(--mut);font:var(--step--1)/1.5 var(--ui);font-variant-numeric:tabular-nums}
article{padding-block:var(--space-m);border-block-start:1px solid var(--line)}
h2+article{border-block-start:0}
.ch{display:flex;flex-wrap:wrap;align-items:baseline;gap:.3rem var(--space-s)}
.ex{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,24rem),1fr));gap:var(--space-s)}
figure{--tone:var(--mut);border-block-start:2px solid var(--tone)}
figure.fail{--tone:var(--bad)}figure.pass{--tone:var(--good)}
figcaption{padding-block:.3rem;color:var(--tone);font:700 var(--step--1)/1.3 var(--ui)}
figure pre{background:color-mix(in oklch,var(--tone) 7%,var(--bg));border-radius:0;white-space:pre-wrap;overflow-wrap:anywhere}figure pre code{overflow-wrap:anywhere}
article:target>.ch h3{text-decoration:underline;text-decoration-color:var(--acc);text-decoration-thickness:.15em;text-underline-offset:.2em}
footer{margin-block-start:var(--space-l);padding-block:var(--space-s) var(--space-m);border-block-start:1px solid var(--line);color:var(--mut);font:var(--step--1)/1.5 var(--ui)}
.fl{display:flex;flex-wrap:wrap;gap:0 var(--space-m);margin:0;padding:0;list-style:none}.fl a{display:flex;align-items:center;min-block-size:44px}
@media(hover:hover) and (pointer:fine){
a:hover{text-decoration-thickness:.16em}nav a:hover,summary:hover{color:var(--acc)}nav details>div a:hover{background:color-mix(in oklch,var(--fg) 8%,transparent)}
button:hover{border-color:var(--fg)}ul.ck li:not(.th):hover{background:color-mix(in oklch,var(--fg) 4%,transparent)}
}
@media(max-width:40rem){.lab{inline-size:100%}}
@media(prefers-reduced-motion:no-preference){
html{scroll-behavior:smooth}button{transition:transform 140ms var(--ease-out),background-color .15s,border-color .15s}
}"""
JS = """const q=s=>[...document.querySelectorAll(s)],$=i=>document.getElementById(i),K={c:'concern',t:'topic',l:'level'},S={c:new Set(),t:new Set(),l:new Set()},
E=$('empty'),D=$('dsum'),C=$('count'),H=$('share'),R=$('grp'),X=$('clr'),F=$('flat'),Q=$('grouped'),have={c:new Set(),t:new Set(),l:new Set()};let G='';
q('button[data-k]').forEach(b=>have[b.dataset.k].add(b.dataset.v));
{const p=new URLSearchParams(location.search);
for(const k in K)p.getAll(K[k]).flatMap(v=>v.split(',')).map(v=>v.trim().toLowerCase()).forEach(v=>have[k].has(v)&&S[k].add(v));
if(R){q('#grp option').forEach(o=>o.value&&p.get('group')==o.value&&(G=o.value))}}
const tg=a=>a.dataset.tags.split(' ');
function group(rows){Q.hidden=!G;F.hidden=!!G;if(!G){Q.textContent='';return}
const k=G[0],vals=[...have[k]].filter(v=>!S[k].size||S[k].has(v)),th=F.querySelector('.th');
const mine=(a,v)=>k=='l'?a.dataset.level==v:tg(a).includes(v),other=rows.filter(a=>!vals.some(v=>mine(a,v)));
Q.textContent='';
[...vals.map(v=>[v,rows.filter(a=>mine(a,v))]),['no '+G,other]].forEach(([v,rs])=>{if(!rs.length)return;
const w=document.createElement('div'),h=document.createElement('h3'),u=document.createElement('ul');w.className='ckw';h.className='gh';h.textContent=v+' ('+rs.length+')';u.className='ck';
u.append(th.cloneNode(true),...rs.map(a=>{const c=a.cloneNode(true);c.removeAttribute('id');return c}));w.append(h,u);Q.append(w)})}
function go(sync){q('[data-tags]').forEach(a=>{const g=tg(a);
a.hidden=(S.c.size>0&&![...S.c].some(x=>g.includes(x)))||(S.t.size>0&&![...S.t].some(x=>g.includes(x)))||(S.l.size>0&&!S.l.has(a.dataset.level))});
const on=S.c.size+S.t.size+S.l.size>0,rows=q('#flat li[data-tags]:not([hidden])'),s=rows.length,d=q('details [data-tags]:not([hidden])').length;
if(E){E.hidden=!on||s>0;E.textContent='No stable cards match.'+(d?' '+d+' draft '+(d>1?'cards match':'card matches')+' below.':'')}
if(D)D.textContent=D.dataset.n+' draft cards'+(on?' ('+d+' match)':'')
if(C)C.textContent=on?s+' stable and '+d+' draft '+(s+d==1?'card matches.':'cards match.'):'';
q('details.fg').forEach(d=>{const n=S[d.dataset.k].size;d.querySelector('.sel').textContent=n?'('+n+' selected)':''});
if(X)X.hidden=!on&&!G;if(R){R.hidden=false;R.value=G}
if(F)group(rows);
if($('gnote'))$('gnote').hidden=!(G=='concern'||G=='topic');
const p=[...Object.keys(K)].filter(k=>S[k].size).map(k=>K[k]+'='+[...S[k]].join(',')),g=G?['group='+G]:[],qs=[...p,...g].join('&');
if(sync)history.replaceState(null,'',location.pathname+(qs?'?'+qs:'')+location.hash);
if(H){const m=H.dataset.md;H.hidden=!qs;H.textContent='';if(qs){H.append('This view: ');
const add=(t,h)=>{const a=document.createElement('a');a.href=h;a.textContent=t;H.append(a)};add('?'+qs,'?'+qs);
if(m){H.append(' · as text for agents: ');add(m+'.md','/'+m+'.md?'+[...p,...g].join('&'));H.append(' · as JSON: ');add('cards.json','/cards.json?'+p.join('&'))}}}}
q('button[data-k]').forEach(b=>{const s=S[b.dataset.k],v=b.dataset.v;b.setAttribute('aria-pressed',s.has(v));
b.onclick=()=>{s.has(v)?s.delete(v):s.add(v);b.setAttribute('aria-pressed',s.has(v));go(1)}});
if(R)R.onchange=()=>{G=R.value;go(1)};
if(X)X.onclick=()=>{Object.values(S).forEach(s=>s.clear());G='';q('button[data-k]').forEach(b=>b.setAttribute('aria-pressed',false));go(1)};
q('details.fg').forEach(d=>{if(S[d.dataset.k].size)d.open=true});
if(matchMedia('(max-width:40rem)').matches)q('details.fg').forEach(d=>{if(!S[d.dataset.k].size)d.open=false});
go();
const V=document.getElementById('said'),say=(b,m)=>{b.textContent=m;V.textContent=m+'.'};
q('button[data-copy]').forEach(b=>{const l=b.textContent;b.hidden=false;b.onclick=()=>{
const t=b.dataset.copy=='ck'?q('#flat li[data-tags]:not([hidden])').map(r=>'- `'+r.querySelector('a').textContent+'` ['+r.querySelector('.b').textContent+'] '+r.querySelector('.r').textContent+' PASS/FAIL/N/A: ').join('\\n'):b.previousElementSibling.textContent;
(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>say(b,'Copied'),()=>say(b,'Copy failed'));setTimeout(()=>{b.textContent=l;V.textContent=''},1500)}});
const op=()=>{const e=document.getElementById(location.hash.slice(1)),d=e&&e.closest('details');if(d){d.open=true;e.scrollIntoView()}};
addEventListener('hashchange',op);op()"""
# WebMCP (https://webmachinelearning.github.io/webmcp/): read-only tools over the page's own content. No network call, storage, or form (tools/agent_ready_check.py item 34).
JS += """
{const m=document.modelContext||navigator.modelContext;
if(m&&m.registerTool){const o=location.origin,t=(name,description,properties,run)=>m.registerTool({name,description,inputSchema:{type:'object',properties},annotations:{readOnlyHint:true},
execute:async a=>JSON.stringify(run(a||{}))}).catch?.(()=>0);
t('start_review','The prompt and the entry file for reviewing code with Good Code Review.',{},()=>({prompt:'Read '+o+'/llms.txt and use it to review my code.',llms_txt:o+'/llms.txt',agent_manifest:o+'/agent.json'}));
t('list_levels','The review levels. Pick the one that matches the input: a diff, file, package, service, design, repo, release, or incident.',{},()=>__LEVELS__.map(l=>({level:l,page:o+'/'+l,markdown:o+'/'+l+'.md',cards:o+'/cards/'+l+'.json'})));
if(q('[data-tags]').length)t('list_cards','The stable cards on this page, optionally filtered by concern, topic, or level.',
{concern:{type:'string'},topic:{type:'string'},level:{type:'string'}},a=>q('#flat li[data-tags]').filter(r=>[a.concern,a.topic].every(v=>!v||r.dataset.tags.split(' ').includes(v))&&(!a.level||r.dataset.level==a.level))
.map(r=>({id:r.querySelector('a').textContent,severity:r.querySelector('.b').textContent,rule:r.querySelector('.r').textContent,url:r.querySelector('a').href})))}}
""".replace("__LEVELS__", json.dumps([str(lv) for lv in LEVELS]))
# The site icon: served as /favicon.svg, with tools/favicon.ico (32x32, rendered from this art with rsvg-convert and magick) as /favicon.ico.
FAVICON_SVG = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><rect width='16' height='16' rx='3' fill='#006469'/>"
               "<path d='M3.5 8.5l3 3 6-6' fill='none' stroke='#fff' stroke-width='2'/></svg>\n")
