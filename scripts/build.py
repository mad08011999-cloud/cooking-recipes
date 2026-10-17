import json, re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from curated import R
src = sys.argv[1] if len(sys.argv) > 1 else "/tmp/cr/data/recipes-01.json"
repo = json.load(open(src))
orig = json.load(open(os.path.join(os.path.dirname(__file__), "origins_raw.json")))
from origins import ORIGINS
EXTRA_STEPS = {
 "biryani": ["★ Meanwhile, parboil the soaked rice in salted water with a bay leaf, cinnamon, cloves and cardamom until 70% cooked; drain.",
             "★ Layer the rice over the cooked lamb, top with fried onions, fried cashews, mint, cilantro, the saffron milk and ghee.",
             "★ Cover tightly and cook on the lowest heat (dum) for 20–25 minutes. Rest 10 minutes and serve with raita."],
 "chicken-fried-rice": ["★ Cook the chicken until browned and cooked through, 4–5 minutes; remove.",
             "★ Add the last tablespoon of oil, then onion, garlic, ginger and carrot; stir-fry 2 minutes, then the peas.",
             "★ Add the cold rice, five-spice and soy sauce; toss on high heat 3–4 minutes.",
             "★ Return chicken and eggs, add scallions and sesame oil, toss and serve."],
}
EXTRA_ING = {"biryani": [["2", "tomatoes, chopped (★ used in steps)"], ["2", "green chillies (★ used in steps)"], ["as needed", "oil for frying onions (★)"], ["to taste", "salt (★)"]]}
def clean_step(s):
    s = re.sub(r"^Prep:.*?Ready in:\s*\d+\s*min\s*", "", s).strip()
    s = re.sub(r"^\d\s+(?=[A-Z])", "", s)
    s = re.sub(r"^Q(?=Make)", "", s)
    s = re.sub(r"\.\s+\d\s+(?=[A-Z])", ". ", s)
    return s
def bad_step(s):
    return s.startswith("{") or (s.islower() and len(s.split()) > 8 and "." not in s)
out = []
for rp in repo:
    c = dict(R[rp["id"]])
    ing = c["ingredients"]
    if ing is None:
        ing = [[i["measure"], i["item"]] for i in rp["ingredients"]]
        seen=set(); dedup=[]
        for q,i in ing:
            key=(q,i)
            if key in seen: continue
            seen.add(key); dedup.append([q,i])
        ing = dedup
        if rp["id"]=="chocolate":
            ing = [[q, "Baking Soda" if (i=="Baking Powder" and any(x[1]=="Baking Powder" for x in ing[:k])) else i] for k,(q,i) in enumerate(ing)]
            ing = [[q,i] for q,i in ing]  # (duplicate baking powder in source -> soda per the steps)
    ing = ing + EXTRA_ING.get(rp["id"], [])
    steps = c["steps"]
    if steps is None:
        steps = [clean_step(s) for s in rp["steps"] if not bad_step(s)]
    steps = steps + EXTRA_STEPS.get(rp["id"], [])
    o = orig.get(rp["id"], {})
    keep_media = c["mode"] in ("repo", "completed") and rp.get("recipe_source") == "themealdb"
    post = {}
    if rp.get("calories_source") == "from post": post["kcal"] = rp["calories"]
    if rp.get("time_source") == "from post": post["time_min"] = rp["time_min"]
    c.update(ingredients=ing, steps=steps, total=c["prep"] + c["cook"],
             repo=dict(name=rp["name"], category=rp["category"], cuisine=rp["cuisine"], best_time=rp["best_time_to_cook"],
                       saved_count=rp["saved_count"], source=rp["recipe_source"], post=post,
                       time_min=rp["time_min"], time_source=rp["time_source"], calories=rp["calories"], calories_source=rp["calories_source"],
                       n_ing=len(rp["ingredients"]), n_steps=len(rp["steps"])),
             image=rp["image"] if keep_media else None, youtube=rp["youtube"] if keep_media else None,
             saved=rp["saved_count"],
             origin=dict(place=o.get("place"), place_title=o.get("place_title"), place_desc=o.get("place_desc"),
                         place_extract=o.get("place_extract"), place_url=o.get("place_url"), image=o.get("image"),
                         dish_title=o.get("dish_title"), dish_extract=o.get("dish_extract"), dish_url=o.get("dish_url")))
    out.append(c)
assert len(out) == len(repo)
json.dump({"generated_from": "github.com/poojithmalla8/cooking_recipe (data/recipes-01.json)", "count": len(out), "recipes": out},
          open("recipes.json", "w"), ensure_ascii=False, indent=0)
print(len(out), "recipes")
for c in out: print(c["id"], c["mode"], len(c["ingredients"]), len(c["steps"]), bool(c["image"]))
