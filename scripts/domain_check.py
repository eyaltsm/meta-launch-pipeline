"""Read-only domain check: availability and price for name x TLD combinations.

Usage: python domain_check.py vanish vanishwallet --tlds com,app,xyz,fun,tech
Uses Porkbun's public pricing API, a DNS lookup, and (if keys exist in ~/.config/porkbun/.env)
Porkbun's authenticated checkDomain for the exact price. Never buys anything, never prints keys.
"""
import argparse, json, os, subprocess, urllib.request, urllib.error

def porkbun(path, keys, extra=None):
    body = dict(keys or {}); body.update(extra or {})
    req = urllib.request.Request("https://api.porkbun.com/api/json/v3/" + path, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
    try:
        return json.load(urllib.request.urlopen(req, timeout=30))
    except urllib.error.HTTPError as e:
        return {"status": "ERROR", "http": e.code}

def load_keys():
    p = os.path.expanduser("~/.config/porkbun/.env")
    if not os.path.exists(p):
        return None
    env = {}
    for line in open(p, encoding="utf-8"):
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.strip().split("=", 1)
            env[k.strip()] = v.strip().strip("'\"")
    if env.get("PORKBUN_API_KEY") and env.get("PORKBUN_SECRET_KEY"):
        return {"apikey": env["PORKBUN_API_KEY"], "secretapikey": env["PORKBUN_SECRET_KEY"]}
    return None

def dns_free(domain):
    out = subprocess.run(["nslookup", "-type=NS", domain, "1.1.1.1"], capture_output=True, text=True, timeout=20)
    text = out.stdout + out.stderr
    return "Non-existent domain" in text or "NXDOMAIN" in text

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="+")
    ap.add_argument("--tlds", default="com,app,xyz,fun,tech,io,sh,trade")
    a = ap.parse_args()
    pricing = porkbun("pricing/get", None).get("pricing", {})
    keys = load_keys()
    rows = []
    for n in a.names:
        for t in a.tlds.split(","):
            d = f"{n}.{t}"
            if t not in pricing or not dns_free(d):
                continue
            exact = porkbun(f"domain/checkDomain/{d}", keys).get("response") if keys else None
            if exact and exact.get("avail") != "yes":
                continue
            reg = (exact or {}).get("price") or pricing[t]["registration"]
            renew = ((exact or {}).get("additional", {}).get("renewal", {}) or {}).get("price") or pricing[t]["renewal"]
            rows.append((float(reg), d, reg, renew, "confirmed" if exact else "dns hint"))
    for _, d, reg, renew, how in sorted(rows):
        print(f"{d:28} first year ${reg:<8} renews ${renew:<8} {how}")
    if not rows:
        print("nothing free in that set")

if __name__ == "__main__":
    main()
