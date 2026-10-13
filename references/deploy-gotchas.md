# Deploy gotchas (each one cost time on VANISH)

## Vercel
- **Invalid `vercel.json` breaks everything.** A regex with `\.` inside a JSON string must be written `\\.`. Validate with `python -c "import json;json.load(open('vercel.json'))"` before deploying.
- **Only the deployed folder is uploaded.** If `web` imports `../engine`, the cloud build cannot find it. Copy the engine into `web/engine-vendor` before each deploy (`scripts/vendor-engine.mjs` + a `deploy:prod` npm script) and let the Vite alias and tsconfig paths fall back to it when `../engine` is missing.
- **Team default "Vercel Authentication" blocks the public.** Disable it per project: write `{"ssoProtection":null}` to a file and run `vercel api /v9/projects/<name> -X PATCH --scope <team> --input <file>` from a directory that has no `api` folder.
- **Git Bash rewrites `/v9/...` into a Windows path.** Prefix with `MSYS_NO_PATHCONV=1`, and pass `--input` a relative file path.
- **`vercel link` writes a `VERCEL_OIDC_TOKEN` into `.env.local`.** Make sure `.env*` is in `.vercelignore` and `.gitignore`.
- **`VITE_` variables are baked in at build time.** Changing them on Vercel does nothing until the next deploy. `vercel env pull` shows sensitive values as empty; verify by grepping the deployed JS chunks for `VITE_NAME:"value"` instead.
- **Add env values from a script** (`vercel env add NAME production --sensitive --force` with the value on stdin) so secrets never appear in output.
- **Service worker:** serve `/sw.js` with `Cache-Control: no-cache, no-store, must-revalidate`, keep a `?sw=off` kill switch, never cache `/api/*` or RPC.

## Domain and DNS (Porkbun API, keys in `~/.config/porkbun/.env`)
- `domain/checkDomain/<d>` gives the real price, promo flag and renewal. Show the renewal price to the founder; promos hide it.
- `domain/create/<d>` with `{"cost": <pennies>, "agreeToTerms": "yes"}` is a purchase: only with the founder's explicit yes in chat, and the cost field caps it at the quoted price.
- DNS for Vercel: `A @ 76.76.21.21` and `CNAME www cname.vercel-dns.com`, then `vercel domains add <d> <project>` and `vercel domains verify`.
- Domains not opted in to API access cannot be changed through the API (for example auto-renew); the founder flips those in the dashboard.

## After every deploy, verify live
- Every route returns 200, the RPC proxy answers for the site origin, refuses a foreign origin and a blocked method, a repeat call shows `x-cache: hit`, the market proxy answers, `/sw.js` has no-cache, and the downloaded JS chunks contain zero key references.
- One headless render of the main app at desktop and phone width with zero console errors.

## Machine hygiene
- The build machine's disk filled up mid-build (1 GB free). Check `df -h /c` before renders. Safe cleanups: `npm cache clean --force`, `pnpm store prune`, `pip cache purge`, crash dumps. Ask before Docker, model caches or old Playwright browsers.
- Never run `taskkill /IM chrome.exe` or similar blanket kills; close only the browsers you launched.
