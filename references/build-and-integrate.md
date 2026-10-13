# Building 5+ features in parallel, then integrating

## Before launching agents
1. Project layout that worked: `projects/<slug>/{brand,engine,web,video}`. `engine` is a TypeScript library with its own tests; `web` is Vite + React + TypeScript consuming it through an `@engine` alias.
2. Create one stub folder per feature (`web/src/features/<slug>/index.tsx` exporting a placeholder) and register every route in `features/registry.ts` before any agent starts. Agents then never touch shared files.
3. Copy `assets/BUILD-RULES.template.md` to `projects/<slug>/BUILD-RULES.md` and fill in the project specifics.
4. Assign each agent a port (5191, 5192, ...). Tell it to run `npx vite --port <n>` itself in the background and stop it afterwards.
5. Launch all independent agents in one message, Sonnet, effort medium. One agent owns the main app surface and shared styles; the rest own only their folder.

## The brief for each feature agent
- What the feature does, in user terms, and the honest limits it must state.
- The named exports the integration needs (a page plus embeddable panels and hooks), documented in the folder README.
- Real data sources and how to stay inside rate limits.
- Tests to write (in the shared test folder; the vitest config only picks up that folder unless merged).
- How to verify: real data, desktop and 390px screenshots that it looks at, console errors.
- Never send a mainnet transaction; throwaway keys; mocked Connection for live paths.

## Integration checklist (do it yourself)
- Fill the main surface's extension slots with thin adapter components (one file each, default export taking the shared context).
- Navigation: keep the strip to about 7 key surfaces plus an "All tools" page generated from the registry.
- Landing: feature the best 6 with honest limits and link to all tools.
- The main app should show live data before a wallet exists; put create/unlock in the trade column, not as a full-page wall.
- Layout trap: a flex column whose children may shrink lets a tab panel collapse to zero height and paint over its neighbours. Give side columns `flex-shrink: 0` children and let the column scroll.
- One `npm test`, `tsc -b`, lint and build all green. Then a headless QA pass of every route at 1440 and 390.

## Rate limits (design them in from the start)
- Never put an RPC or data key in a `VITE_` variable; it ships to every browser.
- Server-side proxy `api/rpc.js`: method allowlist, origin check, batch cap, upstream list (primary, then fallback on 429/5xx), per-item cache for immutable answers (confirmed transactions 10 min, holder lists 30 s), `x-cache` header.
- Dev server proxy reads the same keyed upstream from a non-`VITE_` var in `.env.local`.
- Read transactions in JSON-RPC batches (10 per request) instead of one call each; retry failed items once more, slowly, then mark the result incomplete below 90 percent coverage.
- Market data (DexScreener, GeckoTerminal) through a cached GET proxy (`api/market.js`) in production. GeckoTerminal 429 responses carry no CORS headers, so the browser reports them as network errors; treat those as rate limits.
- Charts: candles are market data, not chain data. An RPC key (Alchemy, Helius) cannot provide them. Fall back to DexScreener's embeddable chart when the candle feed is throttled.
- Alchemy's Solana endpoint supports every method a wallet terminal needs and JSON-RPC batches. Helius has an enhanced history endpoint (about 100 parsed transactions per call) worth using for scanners.
