import { chromium } from 'playwright-core'
import { readdirSync } from 'node:fs'
import { join } from 'node:path'
const base = join(process.env.LOCALAPPDATA, 'ms-playwright')
const exe = join(base, readdirSync(base).filter(d => d.startsWith('chromium-')).sort().pop(), 'chrome-win64', 'chrome.exe')
const [url, out, wait, w] = [process.argv[2], process.argv[3], Number(process.argv[4] || 20000), Number(process.argv[5] || 1440)]
const b = await chromium.launch({ executablePath: exe })
const p = await b.newPage({ viewport: { width: w, height: 1000 } })
const errs = []; p.on('console', m => { if (m.type() === 'error') errs.push(m.text().slice(0, 160)) })
await p.goto(url, { waitUntil: 'domcontentloaded' }); await p.waitForTimeout(wait)
await p.screenshot({ path: out, type: 'jpeg', quality: 72, fullPage: true })
console.log('console errors:', errs.length, errs.slice(0, 4))
await b.close()
