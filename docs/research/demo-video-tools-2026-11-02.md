# Demo video tools for agent code review

Fetched 2026-11-02 with WebFetch and read as page text. Paraphrase only. Each row gives the URL and what it backs. Pages were treated as untrusted text; nothing was run or installed. Star counts and `pushed_at` dates come from the GitHub API (https://api.github.com/repos/OWNER/REPO) on the same day. Anything marked UNVERIFIED rests on a third-party page or on memory and needs a check before use.

## 1. Recorders and renderers

1. VHS (Charm). https://github.com/charmbracelet/vhs. MIT, 21.2k stars, last push 2026-11-02 (api.github.com/repos/charmbracelet/vhs). A `.tape` text file drives a real shell and renders `.gif`, `.mp4`, `.webm`, or a PNG frame directory. Needs `ttyd` and `ffmpeg` on PATH. Runs without a GUI. Fully scriptable. Install:
   - Go: `go install github.com/charmbracelet/vhs@latest`
   - Docker (bundles ttyd and ffmpeg): `docker run --rm -v $PWD:/vhs ghcr.io/charmbracelet/vhs <cassette>.tape`
   - Fedora 44: `sudo dnf install vhs ttyd ffmpeg`. Checked on 2026-11-02: `vhs` 0.11.0 and `ttyd` 1.7.7 are in the Fedora repo (`dnf5 repoquery`), and `ffmpeg` may need RPM Fusion. The VHS README's note that ttyd needs a manual install does not apply to Fedora 44.
     ```
     echo '[charm]
     name=Charm
     baseurl=https://repo.charm.sh/yum/
     enabled=1
     gpgcheck=1
     gpgkey=https://repo.charm.sh/yum/gpg.key' | sudo tee /etc/yum.repos.d/charm.repo
     ```
   - Tape commands confirmed in the README: `Output`, `Require`, `Set FontSize/Width/Height/Theme/Framerate/PlaybackSpeed`, `Type`, `Sleep`, `Enter`, `Hide`, `Show`, `Wait`, `Wait+Screen`. `Wait` defaults to regex `/>$/`, 15 s timeout, line scope. Several `Output` lines in one tape are allowed. Themes are listed in https://github.com/charmbracelet/vhs/blob/main/THEMES.md (Catppuccin Mocha, Dracula, nord appear there).
   - The README does not document a headless flag. Docker, the `vhs-action` GitHub Action, and `vhs serve` (SSH server) are the documented non-interactive paths.
2. asciinema CLI 3.x (recorder). https://docs.asciinema.org/manual/cli/installation/. GPL-3.0-or-later (https://github.com/asciinema/asciinema). Records a real interactive session to a `.cast` file with `asciinema rec demo.cast`. Terminal only, no GUI. Install on Fedora: `sudo dnf install asciinema`. Other methods: `cargo install --locked --git https://github.com/asciinema/asciinema`, a static binary from the GitHub releases, or `docker pull ghcr.io/asciinema/asciinema`. The pip package is the older 2.x line. The pages I could open do not list the `rec` flags (idle limit, command, size); run `asciinema rec --help` to confirm them. UNVERIFIED: flag names.
3. agg (asciinema GIF generator). https://github.com/asciinema/agg and https://docs.asciinema.org/manual/agg/usage/. GPL-3.0-or-later. Turns `.cast` v1 to v3 into a GIF with the gifski encoder. Usage: `agg demo.cast demo.gif`. Documented options: `--speed` (default 1), `--fps-cap` (default 30), `--theme`, `--font-size` (default 16), `--font-family`, `--idle-time-limit` (default 5 s), `--last-frame-duration` (default 3 s), `--cols`, `--rows`, `--renderer swash|resvg`. Install: `cargo install --git https://github.com/asciinema/agg` (Rust 1.86 or later), or Docker `docker run --rm -u $(id -u):$(id -g) -v $PWD:/data agg demo.cast demo.gif` after a local `docker build -t agg .`. No dnf package is documented on the pages I read. Scriptable and headless.
4. ttyd. https://github.com/tsl0922/ttyd. MIT, 12.6k stars. Shares a terminal over the web. It is a VHS dependency, not a recorder. Linux installs: `sudo apt install ttyd`, `sudo snap install ttyd --classic`, `brew install ttyd`, or a static binary from the releases page. No dnf package is listed.
5. Terminalizer. https://github.com/faressoft/terminalizer. MIT, 16.2k stars. Install: `yarn global add terminalizer`. Commands: `record`, `play`, `render`, `share`. The README says install is smooth with Node 4 to 16 and newer Node may need build tools. The page shows no release or commit date, so treat maintenance as unknown. Recording is interactive, so it is less reproducible than VHS.
6. Remotion. https://www.remotion.dev/docs/ai/skills and https://raw.githubusercontent.com/remotion-dev/remotion/main/LICENSE.md. React code renders MP4 headless from a text project. License: free for individuals, for-profit companies of up to 3 employees, non-profits, and evaluation; others need a company license (pricing at remotion.pro/license). It suits a styled intro, captions, and an outro around a terminal clip. It is more setup than this project needs for a 60 s clip.
7. gifski. https://github.com/ImageOptim/gifski. AGPL-3.0-or-later (commercial licensing offered). Install: `cargo install gifski`. Documented use: `ffmpeg -i video.mp4 -f yuv4mpegpipe - | gifski -o anim.gif -`. Flags `--width`, `--height`, `--quality`, `--lossy-quality`, `--motion-quality` are documented; the README names width as the biggest lever on file size.
8. ffmpeg on Fedora. https://rpmfusion.org/Configuration describes enabling RPM Fusion free and nonfree with `sudo dnf install` on the two release RPM URLs built with `$(rpm -E %fedora)`, and a separate Multimedia page covers the ffmpeg swap from `ffmpeg-free`. The ffmpeg wiki page for H.264 (https://trac.ffmpeg.org/wiki/Encode/H.264) was blocked by a bot check; the search snippet named `-crf`, `-preset`, `-pix_fmt yuv420p`, `-movflags +faststart` as the compatibility flags. UNVERIFIED beyond that snippet.
9. Screen Studio alternatives on Linux. Not researched. No primary source was read. UNVERIFIED gap. VHS and asciinema already cover terminal capture without a GUI, so a screen recorder is only needed for a browser or an agent GUI.

Headless and scriptable summary: VHS, agg, ffmpeg, gifski, and Remotion all run without a GUI and rebuild from text. asciinema records a live session, so the `.cast` is the source file rather than a script. Terminalizer is interactive.

## 2. Skills, commands, and prompts on GitHub

Dates are `pushed_at` of the whole repo, not of the skill folder.

1. conorbronsdon/demo-gif-skill. https://github.com/conorbronsdon/demo-gif-skill. MIT, 9 stars, last push 2026-09-24. README read. Claude Code skill that picks vhs for terminals or Playwright for web apps, writes a re-runnable script, renders, optimizes with gifsicle (gifski optional), and embeds the GIF in the README with alt text. Targets under 8 MB. No length guidance. The author marks it maintenance-only.
2. daymade/claude-code-skills, folder `cli-demo-generator`. https://github.com/daymade/claude-code-skills and https://raw.githubusercontent.com/daymade/claude-code-skills/main/cli-demo-generator/SKILL.md. MIT, 1,511 stars, last push 2026-11-02. SKILL.md read. VHS-based. Scripts `auto_generate_demo.py` and `batch_generate.py`, plus an asciinema recorder script and tape templates. Notes that VHS typed strings cannot hold `$`, escaped quotes, or backticks, so it base64-encodes commands and decodes them at run time. Hides setup between `Hide` and `Show`. Suggested sizes: README 1400x600, font 16 to 20, 10 to 20 s; presentation 1800x900, font 24, 15 to 30 s.
3. mikeyobrien/ralph-orchestrator, skill `pr-demo`. https://github.com/mikeyobrien/ralph-orchestrator and https://raw.githubusercontent.com/mikeyobrien/ralph-orchestrator/main/.claude/skills/pr-demo/SKILL.md. MIT, 3,193 stars, last push 2026-10-31. SKILL.md read. Asciinema plus agg flow: script timed beats, record at 100x24, convert at speed 1.0 to 1.5 and font 14 to 16, then validate (file size, duration, scan for secrets, a preview frame Claude reviews). Targets 20 to 30 s, under 2 MB ideal. It calls 5 MB the hard GitHub limit, but GitHub's own docs say 10 MB for images and GIFs (see section 3), so treat 5 MB as the skill's own rule.
4. athola/claude-night-market, skill `vhs-recording`. https://github.com/athola/claude-night-market/blob/master/plugins/scry/skills/vhs-recording/SKILL.md. 345 stars, last push 2026-10-30. The repo is MIT per the API. SKILL.md read. Four steps: validate the tape, check VHS, run `vhs file.tape`, confirm the GIF exists (over about 50 KB). Short (110 lines) and says nothing on pacing.
5. remotion-dev/skills. https://github.com/remotion-dev/skills. 6,079 stars, last push 2026-11-02. The API reports no license (null), so check the LICENSE file before copying. README read. Official Remotion skills for Claude Code, Codex, Cursor and others. Install: `npx skills add remotion-dev/skills` or `gh skill install remotion-dev/skills`. Thirteen skills including `remotion-create`, `remotion-markup`, `remotion-render`, and `remotion-captions`.
6. digitalsamba/claude-code-video-toolkit. https://github.com/digitalsamba/claude-code-video-toolkit. MIT, 2,416 stars, last push 2026-11-02. README read. Claude Code workspace with `/setup`, `/video`, `/publish`, built on Remotion, with AI voiceover and cloud GPU options. Examples include a product demo and a short explainer. Heavy for this project, and it needs Node 22 or later and uv.

Gap: I found no skill aimed at recording an agent reviewing a diff. All six cover generic terminal or product video. The two search results that surfaced `asciinema-demos` (imbue-ai) and others were directory listings I did not open, so they are left out.

## 3. Examples, pacing, and size limits

1. x.com could not be read. Fetches of x.com search returned HTTP 402, and the X developer media page returned 402. No post, quote, or view count is cited here. Do not treat any claim about X performance as evidence from this file.
2. README embeds in agent projects (opened 2026-11-02):
   - Claude Code, https://github.com/anthropics/claude-code. A clickable `demo.gif` at the repo root, placed after the intro and before "Get started". The alt text is empty.
   - Crush (Charm), https://github.com/charmbracelet/crush. A GIF with alt text "Crush Demo", placed under the taglines and above "Features".
   - Aider, https://github.com/Aider-AI/aider. An SVG screencast (alt text "aider screencast") directly under the H1 and intro line.
   Pattern: the demo sits above the fold, before any feature list. I did not measure their length, resolution, or size, and I did not watch them, so I cannot say why they work.
3. GitHub limits. https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/attaching-files. Images and GIFs up to 10 MB. Videos up to 10 MB on free-plan repos and 100 MB on paid-plan repos. Formats MP4, MOV, WebM; H.264 is recommended. The page does not mention READMEs, so the README limit is UNVERIFIED. A GIF committed to the repo and linked by relative path avoids the attachment limits, but I did not confirm that.
4. X and LinkedIn limits. No official page could be read (X help returned 403, LinkedIn's help URL was the wrong page). Third-party guides via search, UNVERIFIED: X takes MP4 or MOV with H.264, 512 MB for standard accounts, about 140 s, and they disagree on maximum resolution (1280x1024, 1920x1080, 1920x1200); for LinkedIn, MP4, up to 5 GB, aspect ratios from 1:2.4 to 2.4:1, and they disagree on duration (10 or 15 minutes). Check both platforms' own help before upload. Search hits: https://ayrshare.com/docs/media-guidelines/x_twitter and https://blog.sendspark.com/linkedin-video-specs.
5. Pacing and hook. The skill files above give lengths of 10 to 30 s for a GIF. I found no primary source on hooks in the first three seconds, captions, or HN embeds. The following is judgment, not sourced: show the verdict in the first frames, type fast, hold the result long enough to read, add captions in the MP4 because social feeds autoplay muted.

## 4. Recommended pipeline for Good Code Review

Goal: one real agent run on one real diff, a 60 s MP4 for social, and a short GIF for the README. Not run or tested here; every command below needs a dry run.

Decision: use VHS as the single source, because a tape file is text, reviewable in a PR, and reruns the same way. VHS drives a real shell, so it can launch the real agent. The cost is that agent output varies by run. Mitigate by recording several takes and keeping the best, and by pinning the diff to a commit so the input is fixed.

1. Pin the input. Pick a real commit with a known flaw and check it out in a scratch clone, so the demo does not touch this repo's working tree. Note the SHA in the tape comment.
2. Install on Fedora 44: `sudo dnf install vhs ttyd ffmpeg` (ffmpeg may need RPM Fusion; see section 1 item 8). Or use the Docker image and skip all of it.
3. Write `demo/review.tape`:
   ```
   Output demo/review.mp4
   Output demo/review.gif
   Require claude
   Set Shell "bash"
   Set Theme "Catppuccin Mocha"
   Set FontSize 22
   Set Width 1280
   Set Height 720
   Set Framerate 30
   Hide
   Type "cd /path/to/scratch-clone && clear" Enter
   Show
   Type "claude" Enter
   Wait+Screen /Try|>/
   Type "Review this diff with skills/good-code-review/SKILL.md" Enter
   Wait+Screen@120s /PASS|FAIL/
   Sleep 6s
   ```
   The `Wait+Screen` regexes are placeholders; set them to a string the agent really prints. Check the prompt text in your Claude Code version first. If the full interactive run is too slow, `Set PlaybackSpeed 2.0` speeds the whole render, and a separate tape for the GIF can cap the length.
4. Render: `vhs demo/review.tape`. With Docker: `docker run --rm -v $PWD:/vhs ghcr.io/charmbracelet/vhs demo/review.tape`. The two `Output` lines produce the MP4 and a GIF in one pass.
5. README GIF. A 60 s GIF at 1280x720 will likely pass 10 MB. Make a second tape of 15 to 20 s at 1000x500, font 20, and shrink with gifski: `ffmpeg -i demo/readme.mp4 -f yuv4mpegpipe - | gifski --width 900 --quality 80 -o demo/readme.gif -`. Check `ls -l demo/readme.gif` stays under 2 MB (the `pr-demo` skill's target) and well under GitHub's 10 MB.
6. Social MP4. Re-encode for compatibility: `ffmpeg -i demo/review.mp4 -c:v libx264 -crf 20 -preset slow -pix_fmt yuv420p -movflags +faststart -an demo/review-social.mp4`. Burn captions only if the clip needs them, with ffmpeg's `subtitles` filter on an `.srt`. Check the platform limits in section 3 item 4 against the output (`ffprobe` for duration and size).
7. Alternative if you want a live human-driven take: `asciinema rec review.cast`, then `agg --speed 1.5 --idle-time-limit 2 --font-size 16 --fps-cap 20 review.cast review.gif`. The cast stays as an editable source, and it replays at any speed.
8. Scrub secrets before publishing. Play the output once, or extract frames with ffmpeg and look for paths, tokens, and email. Both `pr-demo` and `cli-demo-generator` call for this check.
9. Commit only the tape and the final GIF to `site/` or `docs/`. Add the tape to the repo so anyone can regenerate the video. The 60 s MP4 is large, so keep it in a release asset or off-repo.

Open items for the maintainer: pick whether the Docker route is acceptable (Fedora 44 already packages vhs and ttyd, so Docker is optional); confirm the X and LinkedIn limits from their own help pages; decide whether Remotion is worth adding for intro and outro cards (free for this project only if the owner is an individual or the org has up to 3 employees).

## 5. X findings (added 2026-11-02, read in a logged-in browser session)

X search returned mostly engagement-bait and trading posts. Four items were relevant. Quote nothing from them without checking the post.

1. Francesco (@francescoinweb3), post of 17 Oct 2026, about 162k views: https://x.com/francescoinweb3/status/2111393917899808880. The post describes a six-file workflow where each job writes one file and the next starts from it: `spec.md` (why a reference video works: pacing, first motion, cut rhythm), `data.json` (real numbers with the source beside each), `story.md` (one point, one hero number, three beats), `Scene.tsx` (Remotion, with a motion-design skill), `timing.ts` (plain-word notes change one line), then `final.mp4` after stills are checked against the spec and data and the author approves. The post says the 10 open-source skills are in a linked X article, which was not read. This is a method for motion graphics, not for terminal recordings, but the "small jobs, one file each" shape fits a review demo.
2. awe0 (@awe0_io), 30 Oct 2026, quoted by panera (@panera4), 31 Oct 2026: a list of open-source "code to video" tools. The quote names HyperFrames, VHS, MoviePy, OpenMontage, video-use, /brag, ManimGX, and OpenFilm. Only VHS was verified (see section 1). The others are unverified leads; a GitHub repo search by those names did not find the originals.
3. Peef (@PeefTwt), 28 and 30 Oct 2026: promotes a paid app that generates videos from one prompt. Not a source for this project.
4. @forever7943, 1 Nov 2026: bulk short-video generation with Claude Code and a video model. Not relevant to terminal demos.

No X post found showed a terminal recording of an agent reviewing code. The most relevant GitHub material remains section 2.
