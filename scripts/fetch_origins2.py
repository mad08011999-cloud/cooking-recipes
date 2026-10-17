import json, os, re, sys, time, urllib.request, urllib.parse
D = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "RecipeSiteBuilder/1.0 (personal cookbook site; github mad08011999-cloud)"}
CACHE_F = D + "/wiki_cache.json"; CACHE = json.load(open(CACHE_F)) if os.path.exists(CACHE_F) else {}
def get(url):
    if url in CACHE: return CACHE[url]
    for i in range(4):
        try:
            v = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30)); CACHE[url] = v; return v
        except urllib.error.HTTPError as e:
            if e.code == 404: CACHE[url] = None; return None
            time.sleep(2)
        except Exception: time.sleep(2)
    return None
summary = lambda t: get("https://en.wikipedia.org/api/rest_v1/page/summary/" + urllib.parse.quote(t.replace(" ", "_"), safe=""))
def license_of(f):
    q = "https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo&iiprop=extmetadata|url&iiurlwidth=1000&titles=" + urllib.parse.quote("File:" + f)
    j = get(q)
    if not j: return None
    p = list(j["query"]["pages"].values())[0]
    if "imageinfo" not in p: return None
    ii = p["imageinfo"][0]; m = ii.get("extmetadata", {}); cl = lambda s: re.sub("<[^>]+>", "", s or "").strip()
    return {"license": cl(m.get("LicenseShortName", {}).get("value")), "artist": cl(m.get("Artist", {}).get("value"))[:120], "page": ii.get("descriptionurl"), "url": ii.get("thumburl") or ii.get("url")}
OVR = json.load(open(D + "/img_overrides.json"))
FOOD = re.compile(r"dish|food|cuisine|curry|bread|sauce|snack|dessert|rice|sandwich|soup|cake|chicken|noodle|pastry|beverage|drink|confection|stew|salad|condiment|pancake|street|fried|meal|biscuit|cookie|kebab|taco|wrap|flatbread|spice|cheese|pudding|sweet", re.I)
def place_img(title, ps):
    local = "img/places/" + re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-") + ".jpg"
    f = OVR.get(title)
    if not f:
        src = (ps.get("originalimage") or {}).get("source", "")
        parts = src.split("?")[0].split("/"); f = urllib.parse.unquote(parts[-2] if "/thumb/" in src else parts[-1]) if src else None
        if f and (not re.search(r"\.jpe?g$", f, re.I) or re.search(r"flag|map|coat|locator|logo|seal|emblem", f, re.I)): f = None
    if not f: return None
    lic = license_of(f)
    if not lic or not lic["license"] or "fair" in lic["license"].lower(): return None
    if not os.path.exists(local):
        from PIL import Image; import io
        data = urllib.request.urlopen(urllib.request.Request(lic["url"], headers=UA), timeout=60).read()
        im = Image.open(io.BytesIO(data)).convert("RGB"); im.thumbnail((1100, 800)); im.save(local, "JPEG", quality=80, optimize=True, progressive=True)
    return {"src": local, "license": lic["license"], "artist": lic["artist"], "file_page": lic["page"]}
recs = json.load(open("recipes.json"))["recipes"]
out = json.load(open(D + "/origins2_raw.json")) if os.path.exists(D + "/origins2_raw.json") else {}
need_img = []
for r in recs:
    p = r.get("origin_plan")
    if not p: out.pop(r["id"], None); continue
    if r["id"] in out and out[r["id"]].get("plan") == [p["dish"], p["place"], r["name"]]: continue
    ds = None
    nm = re.sub(r"\s*\(.*?\)", "", r["name"]).strip()
    if len(nm.split()) <= 4 and "name not in post" not in r["name"]:
        s = summary(nm)
        if s and s.get("type") == "standard" and FOOD.search((s.get("description") or "") + " " + (s.get("extract") or "")[:200]): ds = s
    if not ds and p["dish"]: ds = summary(p["dish"])
    ps = summary(p["place"])
    if not ps: print("NO PLACE", p["place"]); continue
    img = place_img(ps["title"], ps) if ps["title"] not in OVR else place_img(ps["title"], ps)
    if not img and p["place"] in OVR: img = place_img(p["place"], ps)
    if not img: need_img.append(p["place"])
    out[r["id"]] = {"place": p["label"], "place_title": ps.get("title"), "place_desc": ps.get("description"), "place_extract": ps.get("extract"),
                    "place_url": ps["content_urls"]["desktop"]["page"], "image": img,
                    "dish_title": ds.get("title") if ds else None, "dish_extract": ds.get("extract") if ds else None,
                    "dish_url": ds["content_urls"]["desktop"]["page"] if ds else None, "basis": p["rule"], "plan": [p["dish"], p["place"], r["name"]]}
json.dump(out, open(D + "/origins2_raw.json", "w"), ensure_ascii=False, indent=0)
json.dump(CACHE, open(CACHE_F, "w"))
print(len(out), "need img:", sorted(set(need_img)))
