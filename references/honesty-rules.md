# Honesty rules for product and copy

These are the lines the VANISH build drew, and why. Put the relevant ones into each spec's non-negotiables.

## Product
- **Never hide a token's supply concentration from buyers.** Spreading a creator's supply across fresh wallets, or any "the market cannot see the dev %" feature, deceives the people buying and is the core mechanic of rug pulls. It is also exactly what our own Cluster Radar and GMGN/Axiom "bundled" flags exist to catch, so it burns the brand. Offer the honest alternatives instead: creator identity privacy, a dev bag locked or burned on chain in the same bundle, or a zero-dev-bag fair launch. If the founder insists, decline that part and put the feature on hold rather than build it.
- **Privacy means lowering exposure, not anonymity.** A funding transfer from a known wallet is a public link. Shielded pools hide who deposited but amounts and timing are public and small pools are matchable. Say so in the UI and keep an exposure score that never reaches zero.
- **Non-custodial only.** Keys live in the browser (encrypted vault, forced backup before funding). No server holds user funds. No refunds or reversals are possible; say so.
- **Every money path is gated.** Dry run first (simulate on chain), LIVE only with the env flag, typed confirmation, caps, recovery file before the first send. Caps are the founder's call; an "unlimited" cap is a large number, not Infinity (BigInt math breaks on Infinity).
- **Status labels must be literally true.** A dry rehearsal must never read "Filled"; a "Backed up" badge must reflect the real state. These two bugs both shipped once on VANISH.
- **Heuristics are labeled as heuristics.** One shared transaction between holders is weak evidence (exchanges batch transfers); call something "likely insider" only with a shared funder or a direct transfer. A partial scan (rate-limited reads) is marked incomplete and never stored or acted on.

- **No yield or profit mechanics dressed as utility.** "Agents trade for holders", revenue shares or anything that promises returns is a profit claim (and a securities question). Frame utilities as tools people use, not income.

## Copy (site, videos, posts)
- Never "anonymous", "untraceable", "private swaps", "rug-proof", "guaranteed".
- No prices, market caps, profit claims, launch dates or "soon" for a token that does not exist.
- Videos show real captures of the live product; anything not built is a diagram labeled "In development".
- Every launch post gets an honest-limits reply.
