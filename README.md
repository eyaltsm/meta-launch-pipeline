# meta-launch-pipeline

A Claude Code skill that takes a crypto "meta" idea and turns it into a launched product: brainstorming with Codex, research on what is trending right now, a spec with honest limits, a brand kit, explainer videos, a website, a real utility with 5+ features built by parallel agents, a domain, a deploy, and a plan for X posts.

It was written down from a real build (VANISH, vanishwallet.tech), including every trap that cost time: shared browsers getting hijacked by agents, RPC rate limits, Vercel deploy gotchas, and honesty lines the product and copy should not cross.

## Install

Copy the folder into your Claude Code skills directory:

```bash
git clone https://github.com/eyaltsm/meta-launch-pipeline ~/.claude/skills/meta-launch-pipeline
```

Restart Claude Code. Then say something like "let's make an AI agents meta token with a real utility, brainstorm with codex first". The skill triggers on its own.

## What is inside

| Path | What it is |
|---|---|
| `SKILL.md` | The pipeline: 8 stages, verification rules, hard stops |
| `references/honesty-rules.md` | Product and copy lines not to cross, with the reasons |
| `references/build-and-integrate.md` | How to run 5+ feature agents in parallel and integrate them; rate-limit architecture |
| `references/deploy-gotchas.md` | Vercel, DNS, env and service-worker traps with fixes |
| `assets/BUILD-RULES.template.md` | The rules file every feature agent reads |
| `scripts/shoot.mjs`, `scripts/one.mjs` | Headless screenshots with a local Playwright Chromium |
| `scripts/domain_check.py` | Read-only domain availability and price check (Porkbun) |

## Works best with

Other skills the pipeline calls when they are installed: `hyperframes` (videos), `brandkit`, `design-taste-frontend` and `impeccable` (design), `superpowers` (planning and verification), and an `overnight-automation` style skill if you want it to keep working while you are away. Codex CLI is used for the brainstorm step.

## Hard stops

The skill never moves real funds, sends mainnet transactions, creates repos, deploys, buys domains, launches tokens or publishes posts without your explicit yes. It refuses features that hide a token's supply concentration from buyers.

## License

MIT
