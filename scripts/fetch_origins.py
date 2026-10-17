import json, sys, urllib.request, urllib.parse, os, re, time
sys.path.insert(0, os.path.dirname(__file__))
from origins import ORIGINS
UA={"User-Agent":"RecipeSiteBuilder/1.0 (personal cookbook site; contact via github mad08011999-cloud)"}
def get(url):
    for i in range(4):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=30))
        except Exception as e:
            err=e; time.sleep(2)
    raise err
def summary(t):
    return get("https://en.wikipedia.org/api/rest_v1/page/summary/"+urllib.parse.quote(t.replace(' ','_'),safe=''))
def license_of(fname):
    q="https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo&iiprop=extmetadata|url&iiurlwidth=1000&titles="+urllib.parse.quote("File:"+fname)
    p=list(get(q)["query"]["pages"].values())[0]
    if "imageinfo" not in p: return None
    ii=p["imageinfo"][0]; m=ii.get("extmetadata",{})
    clean=lambda s: re.sub("<[^>]+>","",s or "").strip()
    return {"license":clean(m.get("LicenseShortName",{}).get("value")),"artist":clean(m.get("Artist",{}).get("value"))[:120],
            "page":ii.get("descriptionurl"),"url":ii.get("thumburl") or ii.get("url")}
BAD=re.compile(r"(map|flag|coat|arms|logo|locator|seal|emblem|icon|symbol|svg|montage|collage|location|districts|admin|\.gif|\.tif|png$)",re.I)
OVERRIDE=json.load(open(os.path.join(os.path.dirname(__file__),"img_overrides.json"))) if os.path.exists(os.path.join(os.path.dirname(__file__),"img_overrides.json")) else {}
def fallback_img(place):
    if place in OVERRIDE:
        f=OVERRIDE[place]; lic=license_of(f)
        if lic and lic["license"]:
            local="img/places/"+re.sub(r"[^a-z0-9]+","-",place.lower()).strip("-")+".jpg"
            if not os.path.exists(local):
                open(local,"wb").write(urllib.request.urlopen(urllib.request.Request(lic["url"],headers=UA),timeout=60).read())
            return {"src":local,"license":lic["license"],"artist":lic["artist"],"file_page":lic["page"],"file":f}
        print("  OVERRIDE FAILED",place,f)
    print("  NEED OVERRIDE",place); return None
    q="https://en.wikipedia.org/w/api.php?action=query&format=json&prop=images&imlimit=60&titles="+urllib.parse.quote(place)
    p=list(get(q)["query"]["pages"].values())[0]
    for im in p.get("images",[]):
        f=im["title"].split(":",1)[1]
        if BAD.search(f) or not re.search(r"\.jpe?g$",f,re.I): continue
        lic=license_of(f)
        if not lic or not lic["license"] or "fair" in lic["license"].lower(): continue
        local="img/places/"+re.sub(r"[^a-z0-9]+","-",place.lower()).strip("-")+".jpg"
        if not os.path.exists(local):
            open(local,"wb").write(urllib.request.urlopen(urllib.request.Request(lic["url"],headers=UA),timeout=60).read())
        print("  fallback",place,f,lic["license"])
        return {"src":local,"license":lic["license"],"artist":lic["artist"],"file_page":lic["page"],"file":f}
    return None
os.makedirs("img/places",exist_ok=True)
out={}; cache={}
for rid,(dish,place,label) in ORIGINS.items():
    try:
        ds=summary(dish); ps=cache.get(place) or summary(place); cache[place]=ps
    except Exception as e:
        print("FAIL",rid,dish,place,e); continue
    img=None
    src=(ps.get("originalimage") or {}).get("source")
    if src:
        parts=src.split("?")[0].split("/")
        fname=urllib.parse.unquote(parts[-2] if "/thumb/" in src else parts[-1])
        lic=license_of(fname)
        if lic and lic["license"] and "fair" not in lic["license"].lower():
            ext=os.path.splitext(fname)[1].lower() or ".jpg"
            if ext in (".svg",".png"): ext=".png" if ext==".png" else ext
            local="img/places/"+re.sub(r"[^a-z0-9]+","-",place.lower()).strip("-")+(".jpg" if ext in(".jpg",".jpeg") else ext)
            if ext!=".svg" and not os.path.exists(local):
                data=urllib.request.urlopen(urllib.request.Request(lic["url"],headers=UA),timeout=60).read()
                open(local,"wb").write(data)
            if ext!=".svg": img={"src":local,"license":lic["license"],"artist":lic["artist"],"file_page":lic["page"]}
        else: print("skip img",place,lic and lic["license"])
    if not img or place in OVERRIDE:
        img=fallback_img(place)
    out[rid]={"place":label,"place_title":ps.get("title"),"place_desc":ps.get("description"),"place_extract":ps.get("extract"),
              "place_url":ps["content_urls"]["desktop"]["page"],"image":img,
              "dish_title":ds.get("title"),"dish_extract":ds.get("extract"),"dish_url":ds["content_urls"]["desktop"]["page"],
              "dish_type":ds.get("type")}
    print("ok",rid,ds.get("type"),ds.get("title"),"|",ps.get("title"),bool(img))
json.dump(out,open("scripts/origins_raw.json","w"),indent=1,ensure_ascii=False)
