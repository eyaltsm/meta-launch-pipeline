---
name: meta-launch-pipeline
description: End-to-end pipeline that turns a crypto "meta" idea into a launched product in days - Codex brainstorm, live meta research, honest spec, brand kit, explainer videos, website, a real utility with 5+ depth features built by parallel agents, domain, deploy and a drop plan for X. Use it whenever the founder says things like "let's make a <privacy / AI / launchpad / X> meta token", "build a new meta project", "start another project like VANISH", "make a token with a real utility", "brainstorm with codex then build it", or pastes a one-line idea and wants the whole thing (logo, video, site, utility, mainnet). Also use it to continue or audit a project that was built with it (projects/<slug> with a BUILD-RULES.md). Not for reviving dead projects (use utility-rebrand-factory) and not for a single isolated page or video.
---

# Meta Launch Pipeline

Turns "let's make a <meta> token" into a real, deployed product with a brand, videos, a website and a utility that people can actually use. Distilled from the VANISH build (projects/vanish, vanishwallet.tech, 2026-10-13/14): what worked, in what order, and every trap that cost hours.

The founder's standing rules come first and override anything below if they ever conflict:
- Model routing for subagents is your call; the reference build used Sonnet for agents and Haiku for cheap lookups, effort low to medium. Set yours here.
- No em dashes anywhere (code, copy, docs, commit messages).
- Never name your studio, team or sibling projects in a project's public copy unless you mean to.
- Real data only. No mock rows, invented numbers, fake screenshots presented as real.
- Reply in the founder's language; specs and code in English.
- Hard stops that always need the founder's explicit yes in chat: moving real funds or sending mainnet transactions (you cannot do this yourself at all; the founder signs), creating a repo, deploying, buying a domain, launching a token, publishing posts. One clear "yes / כן" per action type in the session is enough once given for that project.

## If the founder is stepping away
If the founder says they are going to sleep or leaving and wants work to continue, load the `overnight-automation` skill and run this pipeline under it: Codex stands in for design approvals, routine calls are yours, and the hard stops above still wait for the founder. Keep `OVERNIGHT_STATUS.md` in the project folder. When Codex is unavailable, use a second agent as the reviewer.

## Practical setup
- Work from the repo root (the root of your workspace repo); each project lives in `projects/<slug>`.
- Use the Bash tool (Git Bash) for the commands in this skill; they are written in bash syntax. In PowerShell the Codex call is `Get-Content prompt.txt | codex exec -m gpt-5.5 -c model_reasoning_effort=low --skip-git-repo-check -o out.md -`.
- Bundled scripts live at `~/.claude/skills/meta-launch-pipeline/scripts\` (call them by that absolute path).

## Decisions when the founder is not there
Under overnight mode Codex (or a reviewer agent) also makes the Stage 0 calls a founder normally makes: which concept, the name and slug. Rules for that:
- Evidence beats preference: if the live meta research contradicts Codex's top pick, say so in the prompt and let Codex re-rank with the evidence.
- Red-team the chosen concept before building: ask Codex for the single biggest hole (the VANISH equivalent was "a fresh wallet funded from the main wallet is still linked") and design for it in the spec.
- Record every such call in `OVERNIGHT_STATUS.md` so the founder can reverse it cheaply on return.

## The stages

Work through these in order. Each stage ends with something the founder can see. Show progress early (start a local preview as soon as there is UI) and keep the founder's attention on decisions, not on noise.

### Stage 0: Ideate (Codex + live meta)
1. Brainstorm with Codex. The default Codex model fails on this account, so always pass `-m gpt-5.5` and pipe the prompt on stdin (a bare argument makes it wait on stdin and print nothing):
   `codex exec -m gpt-5.5 -c model_reasoning_effort=low --skip-git-repo-check -o out.md - < prompt.txt`
   Ask for 10 distinct concepts with a real token utility, risks, build effort, virality and defensibility, then a ranked top 3.
2. Research the meta right now. DexScreener's public API needs no key (`/token-boosts/top/v1`, `/token-profiles/latest/v1`, `/tokens/v1/solana/<addrs>`, `/latest/dex/search?q=`). GMGN and Axiom need keys we do not have; use web search for the last 2-4 weeks and say how thin the evidence is.
3. Pick a concept, then immediately stress-test it for the obvious hole. In VANISH the founder caught that a "fresh wallet" funded from the main wallet leaves an on-chain link; design for the hole before building, not after.
4. Check name and ticker collisions (DexScreener search) and domain price and availability (`scripts/domain_check.py`; Porkbun's pricing endpoint is public, DNS NXDOMAIN plus RDAP 404 is a strong hint, the registrar's check is final).

### Stage 1: Spec
Write `docs/superpowers/specs/<date>-<slug>-design.md`: intent, evidence, product flow, token utility, honest limits, out of scope, components, risks, success criteria, and a "non-negotiables" list. Present the key decisions and get the founder's direction before code (or Codex's under overnight mode). See `references/honesty-rules.md` for the lines the product and copy must not cross; put the relevant ones into the spec.

### Stage 2: Brand
Logo mark, wordmark, token icon, X avatar and banner, OG image, favicons, `brand.json` (colors, two fonts, voice rules, taglines). Use the `brandkit` and `design-taste-frontend` skills. Look at every PNG yourself before calling it done; check the mark still reads at 16px.

### Stage 3: Explainer video
Load `hyperframes` (mandatory entry). Kokoro local TTS works (voice `am_michael`); if it is not installed, `media-use` sets it up in a throwaway venv in the scratchpad (never in the project). Check free disk space first (`df -h /c`); renders need several GB. Master the voice to about -16 LUFS with peak below -1 dBFS and measure it with `ffmpeg -af ebur128=peak=true`. Deliver 16:9 and 1:1 (feed) plus a short loop. Pull frames at several timestamps and look at them yourself; mid-animation frames can look broken, sample a second time before flagging.

### Stage 4: Website
Landing page with one signature motion that belongs to the brand (VANISH: scanline-sliced letters that dissolve), honest limits section, FAQ, toolkit. Use `design-taste-frontend` and `impeccable`. If the founder asks for polish, do the polish yourself, not through agents.

### Stage 5: The utility, 5+ depth features
The founder's bar: fewer than 5 distinct features is not worth shipping. Depth usually comes from tools around the core utility (scanners, alerts, analytics, recovery, history, automation), not five copies of one idea. If a concept honestly cannot support five meaningful features, say so to the founder and propose a stronger concept instead of padding with filler. Build them in parallel with Sonnet agents, the way that worked:
1. Create stubs and routes first yourself: one folder per feature, a feature registry, one route per feature, so no two agents edit the same file.
2. Write a shared rules file from `assets/BUILD-RULES.template.md` into the project and point every agent at it. It covers ownership lanes, real-data rules, tests in the shared test folder, safety gates, copy rules and visual verification.
3. Give each agent its own dev-server port in the brief and tell it to run vite itself (the preview tool caps servers per folder).
4. Brief each agent with: the feature, the exact exports the integration needs, verification steps, and the "never send a mainnet transaction" rule.
5. Integrate yourself afterwards: fill extension slots, nav, landing, one test command, lint, build, then QA every route at desktop and phone width.
Details and the integration checklist: `references/build-and-integrate.md`.

### Stage 6: Deploy (founder's yes required)
Vercel under your team, domain via the connected Porkbun API with a cost cap, DNS A record to Vercel plus www CNAME, keys only in server-side env vars behind a proxy. The traps (each cost real time on VANISH) are in `references/deploy-gotchas.md`; read it before the first deploy.

### Stage 7: Drops and X
Bio and first post, then a drop plan where each drop is a real, verified feature with its own short video and post text (`video2/POST.md` style: main post under 280 chars plus two honest replies). Videos built from real captures of the live product, never mock-ups; features not built yet only as clearly labeled teasers. Schedule = ship code early behind a release time, unlock on time, post with the founder's approval.

## How to verify (applies to every stage)
- Never trust an agent's self-report on anything visual. Open the screenshots and frames yourself.
- The in-app browser and the Playwright MCP are shared with running agents and get hijacked. For your own checks use a headless browser: `scripts/shoot.mjs` (full-page slices at 1440 and 390) and `scripts/one.mjs` (one page after a wait).
- Test real data paths read-only against mainnet; simulate transactions; never sign.
- Before saying "done", run the full test suite, type check, lint and a production build, and check the built bundle for leaked keys (`grep -rliE 'alchemy|helius|api-key' dist`).

## Reference files
- `references/honesty-rules.md` - product and copy lines not to cross, with the reasons.
- `references/build-and-integrate.md` - parallel-agent recipe, integration checklist, rate-limit architecture.
- `references/deploy-gotchas.md` - Vercel, DNS, env and service-worker traps with fixes.
- `assets/BUILD-RULES.template.md` - the rules file every feature agent reads.
- `scripts/shoot.mjs`, `scripts/one.mjs` - headless captures with the local Playwright Chromium.
- `scripts/domain_check.py` - read-only availability and price check (Porkbun keys from `~/.config/porkbun/.env`, never printed).
