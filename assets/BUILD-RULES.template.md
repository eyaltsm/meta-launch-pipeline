# <PROJECT> build rules for feature agents (read fully before starting)

Project root: <PROJECT_ROOT> (web\ = Vite React TypeScript app, engine\ = TypeScript library).
Read first: <SPEC_PATH>, <OTHER_PROJECT_DOCS>, web\src\App.tsx, web\src\features\registry.ts, one finished feature for patterns (<EXAMPLE_FEATURE>), the signature-motion component (<MOTION_COMPONENT>), web\src\styles\*.css.

## Ownership (many agents work at the same time, stay in your lane)
- You own ONLY: web\src\features\<your-slug>\ (a stub index.tsx exists and is already routed at /tools/<your-slug>), tests in web\test\<your-slug>*.test.ts, optional new files in engine\src\features\<your-slug>\, and any extra files your brief names.
- Do NOT edit: registry.ts, App.tsx, pages\Terminal.tsx, features\wallet\*, shared styles, package.json (avoid new dependencies; if one is truly needed, say so in your reply), or other features. You MAY import from other features read-only (for example features\scanner\lib, features\wallet\lib, features\bench\lib).
- Export a default page from your folder AND named reusable pieces (components and hooks) documented in your folder README.md, so the terminal integration can embed them. Do not do the embedding yourself.

## Quality
- Look: brand palette and fonts from brand/brand.json. Use skills design-taste-frontend and impeccable. The signature motion component only for hero moments, respect prefers-reduced-motion. Dense, useful, not decorative.
- Real data only: no mock rows, no invented numbers. Every panel has loading, empty and error states. Mobile-first.
- Be kind to free APIs and RPC: cache, dedupe, back off on 429, cap requests. RPC calls go through the app's connection hooks (web\src\wallet\useRpc.ts); in production /api/rpc proxies with an allowlist of read methods.
- Tests: use skill superpowers:test-driven-development. Put them in web\test\ (the shared vitest config only picks up web\test\**). `npx tsc -b`, `npm test` and `npm run lint` must pass for your files from web\ (ignore transient errors in other agents' folders).
- Verify visually: from web\ run `npx vite --port <your port>` with Bash run_in_background, open it in the preview browser, exercise your feature with real data, screenshot desktop and mobile and LOOK at the images, check console errors, then stop your server. Use skill superpowers:verification-before-completion before claiming done.

## Safety (non-negotiable)
- NEVER send a real mainnet transaction, never use or ask for real keys. Throwaway keypairs, simulateTransaction, and mocked Connection tests only. Any live path must be gated: VITE_LIVE_ENABLED must be exactly "true", a typed confirmation, per-action caps, a dry run first. Follow web\src\features\reclaim for the pattern.
- Secrets never logged, never in URLs, never persisted in plaintext.
- No deploy, no GitHub repo, no domain or purchase actions.

## Copy rules
- Never say anonymous, untraceable or "private swaps". Say hygiene, break the trail, anti-tracking. State limits honestly in the UI.
- No em dashes anywhere (code comments, UI, docs). Do not name any studio or sibling project.
- No price, market cap or contract address claims for the project token until it has launched.

## Final reply (under 12 lines)
What exists, verified vs not verified, the exports to embed, anything the founder must decide or provide.
