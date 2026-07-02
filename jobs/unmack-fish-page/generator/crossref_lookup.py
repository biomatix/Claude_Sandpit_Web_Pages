"""Look up each reference in CrossRef; cache DOI + canonical title for confident
matches (validated by year and author surname). Resumable via the JSON cache."""
import json, os, re, time, urllib.request, urllib.parse

JOB = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REFS = json.load(open(os.path.join(JOB, "assets", "references_raw.json"), encoding="utf-8"))
CACHE_PATH = os.path.join(JOB, "assets", "references_crossref.json")
cache = json.load(open(CACHE_PATH, encoding="utf-8")) if os.path.exists(CACHE_PATH) else {}
MAIL = "arthur.georges@biomatix.com.au"


def ref_year(ref):
    m = re.search(r"\((\d{4})[a-z]?\)", ref)
    return int(m.group(1)) if m else None


def first_surname(ref):
    m = re.match(r"\s*([A-Za-z][A-Za-z'\-]+)", ref)
    return m.group(1).lower() if m else ""


def crossref_year(item):
    for k in ("issued", "published-print", "published-online", "published"):
        dp = item.get(k, {}).get("date-parts", [[None]])
        if dp and dp[0] and dp[0][0]:
            return dp[0][0]
    return None


def validate(item, ref):
    ry, iy = ref_year(ref), crossref_year(item)
    if ry and iy and abs(ry - iy) > 1:
        return False
    fams = [a.get("family", "").lower() for a in item.get("author", []) if a.get("family")]
    if not fams:
        return False
    rs = first_surname(ref)
    low = ref.lower()
    if rs and any(rs in f or f in rs for f in fams):
        return True
    return any(f in low for f in fams)


def query(ref):
    clean = re.sub(r"[^\x00-\x7f]", " ", ref)[:600]
    q = urllib.parse.urlencode({"query.bibliographic": clean, "rows": 3, "mailto": MAIL})
    req = urllib.request.Request("https://api.crossref.org/works?" + q,
                                 headers={"User-Agent": "HomeOfTheRainbowfish/1.0 (mailto:%s)" % MAIL})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)


def save():
    json.dump(cache, open(CACHE_PATH, "w", encoding="utf-8"), ensure_ascii=False)


for i, ref in enumerate(REFS):
    key = str(i)
    if key in cache:
        continue
    try:
        items = query(ref).get("message", {}).get("items", [])
        result = {"doi": None}
        for it in items:
            if validate(it, ref):
                result = {"doi": it.get("DOI"), "title": (it.get("title") or [""])[0]}
                break
        cache[key] = result
    except Exception as e:
        cache[key] = {"doi": None, "err": str(e)[:80]}
    if i % 25 == 0:
        save()
        print("%d/%d done (%d matched)" % (i, len(REFS),
              sum(1 for v in cache.values() if v.get("doi"))), flush=True)
    time.sleep(0.12)

save()
print("DONE. %d/%d references matched with a DOI" %
      (sum(1 for v in cache.values() if v.get("doi")), len(REFS)))
