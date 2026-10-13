import { chromium } from 'playwright-core'
import { readdirSync } from 'node:fs'
import { join } from 'node:path'
const base = join(process.env.LOCALAPPDATA, 'ms-playwright')
const dir = readdirSync(base).filter(d => d.startsWith('chromium-')).sort().pop()
const exe = join(base, dir, 'chrome-win64', 'chrome.exe')
const [url, tag] = [process.argv[2], process.argv[3] || 'x']
const browser = await chromium.launch({ executablePath: exe })
for (const [w, h] of [[1440, 900], [390, 844]]) {
  const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1, reducedMotion: 'reduce' })
  await page.goto(url, { waitUntil: 'networkidle' })
  // trigger reveals, then settle
  const H = await page.evaluate(() => document.body.scrollHeight)
  for (let y = 0; y < H; y += 500) { await page.evaluate(v => window.scrollTo(0, v), y); await page.waitForTimeout(60) }
  await page.evaluate(() => window.scrollTo(0, 0)); await page.waitForTimeout(800)
  // slice the full page into viewport-height chunks to keep images readable
  const total = await page.evaluate(() => document.documentElement.scrollHeight)
  const step = w > 800 ? 1100 : 1600
  let i = 0
  for (let y = 0; y < total; y += step, i++) {
    await page.screenshot({ path: `shots/${tag}-${w}-${String(i).padStart(2, '0')}.jpg`, type: 'jpeg', quality: 70, fullPage: true, clip: { x: 0, y, width: w, height: Math.min(step, total - y) } })
  }
  console.log(w, 'height', total, 'chunks', i)
  await page.close()
}
await browser.close()
