import re
import json, glob, re, sys, os
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
from status import assess
from rules import DISH_RULES, CUISINE_FALLBACK, CUISINE_NORM, INFER_CUISINE, CATEGORY_RULES, JUNK_NAME_OVERRIDES, clean_name
from curated import R as OLD
from curated2 import STAR, PREV
SRC = sys.argv[1] if len(sys.argv) > 1 else "/tmp/cr2"
A = [r for f in sorted(glob.glob(SRC + "/data/recipes-*.json")) for r in json.load(open(f))]
PREVSTEPS = json.load(open(D + "/prev_repo_steps.json"))
ORIG = json.load(open(D + "/origins_raw.json"))           # 52 original origin panels
for _k in ("noodles", "full-recipe", "coriander-chutney", "pasta"): ORIG.pop(_k, None)   # dish identity changed
ORIG2 = json.load(open(D + "/origins2_raw.json")) if os.path.exists(D + "/origins2_raw.json") else {}
FACTS = {k: v["fact"] for k, v in OLD.items() if v.get("fact")}
MEAT = r"chicken|mutton|lamb|beef|pork|bacon|ham\b|chorizo|sausage|turkey|keema|steak|pepperoni|salami|kodi|murgh|pollo|wings|drums"
FISHR = r"fish|prawn|shrimp|salmon|tuna|crab|lobster|seafood|snapper|cod\b|anchov|basa"
EGG = r"\begg|eggs|anda\b|omelette"
def diet(text):
    t = text.lower()
    if re.search(MEAT, t): return "Non-veg"
    if re.search(FISHR, t): return "Pescatarian"
    if re.search(EGG, t): return "Eggetarian"
    return "Vegetarian"
def grams_main(ings):
    for q, i, h in ings:
        t = (q + " " + i).lower()
        if re.search(MEAT + "|" + FISHR + r"|paneer|tofu|soya", t):
            m = re.search(r"(\d+(?:\.\d+)?)\s*(kg|g|gm|gms|grams|lb|lbs|ibs|pound|pounds|oz)\b", t)
            if m:
                v = float(m.group(1)); u = m.group(2)
                return v * (1000 if u == "kg" else 453.6 if u in ("lb", "lbs", "ibs", "pound", "pounds") else 28.35 if u == "oz" else 1)
    return None
def macros_est(kcal, cat, text):
    t = text.lower()
    if cat in ("Dessert", "Beverage"): p, c = .07, .55
    elif re.search(MEAT + "|" + FISHR + r"|paneer|tofu|soya|egg", t): p, c = .30, .30
    else: p, c = .12, .55
    if re.search(r"rice|biryani|pulao|pasta|noodle|ramen|maggi|bread|bun|wrap|taco|burrito|roti|naan|paratha|toast|sandwich|burger|fries|potato", t) and cat not in ("Dessert",): c = max(c, .45); p = min(p, .25)
    f = 1 - p - c
    fib = 2 if cat in ("Dessert", "Beverage") else (6 if re.search(r"beans|rajma|chole|dal|spinach|palak|cabbage|veg|broccoli|cauliflower", t) else 3)
    return dict(protein=round(kcal * p / 4), carbs=round(kcal * c / 4), fat=round(kcal * f / 9), fiber=fib)
MAINISH = r"biryani|biriyani|rice|pulao|curry|bowl|wrap|pasta|noodle|ramen|masala|korma|handi|kadhai|gravy|thali|meal|dinner|lunch|roll|burger|sandwich|taco|burrito"
def recat(name, cat):
    n = name.lower()
    for rx, c in CATEGORY_RULES:
        if re.search(rx, n):
            if c in ("Entree", "Side Dish") and re.search(MAINISH, n): return cat if cat not in ("Dessert", "Beverage") else "Main Course"
            if c == "Entree" and cat == "Snack": return cat
            return c
    if cat in ("Dessert", "Beverage") and re.search(MAINISH + r"|chicken|paneer|garlic bread", n) and not re.search(r"cake|cookie|brownie|pudding|shake|breakfast|toast|egg", n): return "Main Course"
    return cat
def infer_cuisine(name, cuisine):
    if cuisine: return CUISINE_NORM.get(cuisine, cuisine), False
    n = name.lower()
    for rx, c in INFER_CUISINE:
        if re.search(rx, n): return c, True
    return None, True
def origin_for(rid, name, cuisine):
    if rid in ORIG: return ORIG[rid]
    return ORIG2.get(rid)
def plan_origin(rid, name, cuisine):
    n = name.lower()
    for rx, cz, dish, place, label in DISH_RULES:
        if re.search(rx, n):
            if place: return dict(dish=dish, place=place, label=label, rule=rx)
            break
    base = (cuisine or "").split(" (")[0].split(" /")[0]
    if base in CUISINE_FALLBACK:
        dish, place, label = CUISINE_FALLBACK[base]; return dict(dish=dish, place=place, label=label, rule="cuisine")
    return None
def moods_for(name, cat, total, tags, text):
    n = (name + " " + text).lower(); m = []
    add = lambda k: m.append(k) if k not in m else None
    if cat in ("Dessert", "Beverage"): add("sweet")
    if cat == "Breakfast" or re.search(r"toast|pancake|omelette|bhurji|upma|idli|breakfast", n): add("brunch")
    if re.search(r"biryani|biriyani|haleem|meetha|mandi|korma|shahi|darbari|nawabi|mughlai|kheer", n): add("festive")
    if re.search(r"meal prep|meal-prep|bowls?\b", n): add("mealprep")
    if "High-protein" in tags or "Air fryer" in tags: add("gym")
    if re.search(r"curry|masala|soup|rasam|haleem|korma|bhurji|maggi|ramen|chai|kosha|handi|dal\b|rajma|chole", n): add("rainy")
    if cat in ("Entree", "Snack") or re.search(r"wings|fries|nachos|65|lollipop|popcorn|tender|nugget|manchurian|burger|slider|taco", n): add("movie")
    if re.search(r"maggi|noodle|ramen|fries|sandwich|burger|wrap|toast|egg rice|fried rice", n): add("latenight")
    if total is not None and total <= 25: add("weeknight")
    if cat == "Entree" or re.search(r"tikka|garlic bread|slider|taco|platter|kebab", n): add("party")
    if total is not None and total >= 45 or re.search(r"roast|biryani|lasagn", n): add("weekend")
    if not m: add("weeknight" if (total or 40) <= 35 else "weekend")
    return m[:3]
def tags_for(name, ings, steps, kcal, prot, total, cat):
    t = (name + " " + " ".join(q + " " + i for q, i, h in ings) + " " + " ".join(steps)).lower()
    tg = [diet(name + " " + " ".join(i for q, i, h in ings))]
    if tg[0] == "Vegetarian" and ings and not re.search(r"milk|cheese|paneer|butter|ghee|cream|curd|yogurt|yoghurt|honey|mayo|egg|feta|mozzarella", t): tg[0] = "Vegan"
    if re.search(r"air ?-?fr(y|ier|ied)|airfry", t): tg.append("Air fryer")
    if prot and prot >= 30: tg.append("High-protein")
    if re.search(r"chilli|chili|schezwan|szechuan|spicy|\bhot\b|peri|dragon|jalape|65|sriracha|gochujang|cayenne|karam|pepper chicken|chettinad", t): tg.append("Spicy")
    if total is not None and total <= 20: tg.append("Quick")
    if re.search(r"meal prep|meal-prep", t): tg.append("Meal prep")
    if re.search(r"cream|malai|alfredo|marry me|makhani|butter masala|lababdar|cheese", name.lower()): tg.append("Creamy")
    if re.search(r"\boven|\bbake|baking", t): tg.append("Oven")
    if re.search(r"pani puri|frankie|kathi|kati|roll\b|street|vada|chaat", name.lower()): tg.append("Street food")
    if re.search(r"rice|biryani|biriyani|pulao", name.lower()): tg.append("Rice dish")
    return tg
def difficulty(nsteps, total):
    s = nsteps + (total or 30) / 15
    return "Easy" if s <= 6 else "Medium" if s <= 11 else "Hard"
out = []
for r in A:
    rid = r["id"]; a = assess(r)
    st, ing = a["steps"], a["ing"]
    name = JUNK_NAME_OVERRIDES.get(rid) or clean_name(r["name"]) or r["name"]
    status, note, hidden = a["status"], a["why"], []
    prep = cook = None; serv = None; serv_est = True; nut = None; moods = None; extra = ""
    if status == "missing" and rid in OLD:
        c = OLD[rid]; status = "rewritten"; name = c["name"]
        ing = [[q, i, False] for q, i in c["ingredients"]]; st = c["steps"]
        prep, cook, serv, extra = c["prep"], c["cook"], c["servings"], c["extra"]; nut = dict(c["nutrition"]); moods = c["moods"]
        note = f"The repo entry is still a placeholder ({a['why']}), so a standard recipe matching the dish name is shown."
    elif rid in PREV and a["status"] == "check":
        p = PREV[rid]; status = "repo-prev"; st = PREVSTEPS[rid]; name = p.get("name", name); note = p["note"]
        hidden = a["steps"]
    elif rid in STAR and a["status"] in ("partial", "check"):
        s = STAR[rid]; status = "completed"; name = s.get("name", name); note = s["note"]
        if a["status"] == "check": hidden = a["steps"]
        st = s["steps"]; ing = ing + [[q, i, False] for q, i in s.get("extra_ing", [])]
    elif status == "check":
        hidden = st; st = []
        note = f"The repo’s steps don’t match its ingredients ({a['why']}); they may be from a different post, so they’re shown separately below."
    cat_repo = r["category"]
    cat = STAR.get(rid, {}).get("category") or PREV.get(rid, {}).get("category") or (OLD[rid]["category"] if status == "rewritten" else recat(name, cat_repo))
    cz, cz_inf = infer_cuisine(name, None if (r["recipe_source"] == "themealdb" and a["status"] == "missing") else r["cuisine"])
    if status == "rewritten": cz, cz_inf = OLD[rid]["cuisine"], False
    total = r["time_min"]; tsrc = r["time_source"]
    if status == "rewritten": total = prep + cook; tsrc = "estimated"
    kcal = r["calories"]; ksrc = r["calories_source"]; msrc = "estimated"
    mac = a["macros"]
    if status != "rewritten" and mac.get("kcal"): kcal, ksrc = mac["kcal"], "from post"
    if status == "rewritten":
        kcal, ksrc = nut["kcal"], "estimated"; nm = {k: nut[k] for k in ("protein", "carbs", "fat", "fiber")}
    else:
        est = macros_est(kcal, cat, name + " " + " ".join(i for q, i, h in ing))
        nm = dict(est)
        if mac.get("protein") is not None: nm.update({k: mac[k] for k in ("protein", "carbs", "fat") if k in mac}); msrc = "from post" if all(k in mac for k in ("protein", "carbs", "fat")) else "mixed"
        g = grams_main(ing)
        serv = max(1, min(10, round(g / 160))) if g else None
        txt = " ".join(st + [r.get("name", "")]).lower()
        W = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6}
        mm = re.search(r"\bserves\s+(\d+|two|three|four|five|six)\b", txt) or re.search(r"\b(\d+|two|three|four|five|six)\s+(?:servings|portions|people)\b", txt) or re.search(r"between\s+(two|three|four|five|six|\d+)\s+(?:bowls|plates)", txt)
        if status == 'missing': serv = None; mm = None
        if mm:
            v = mm.group(1); v = W.get(v) or int(v)
            if 1 <= v <= 12: serv = v; serv_est = False
    shown_steps = st
    tags = OLD[rid]["tags"] if status == "rewritten" else tags_for(name, ing, shown_steps, kcal, nm["protein"], total, cat)
    if not moods: moods = moods_for(name, cat, total, tags, " ".join(i for q, i, h in ing))
    meal_ok = r["recipe_source"] == "themealdb" and a["status"] in ("repo", "partial")
    rec = dict(id=rid, name=name, repo_name=r["name"], category=cat, repo_category=cat_repo, cuisine=cz or "Unspecified", cuisine_inferred=cz_inf and bool(cz),
               repo_cuisine=r["cuisine"], status=status, note=note, ingredients=ing, steps=shown_steps, other_steps=hidden,
               total=total, time_source=tsrc, prep=prep, cook=cook, extra=extra, servings=serv, serv_source=('from recipe' if not serv_est else 'est'), difficulty=OLD[rid]["difficulty"] if status == "rewritten" else difficulty(len(shown_steps), total),
               nutrition=dict(kcal=kcal, **nm), kcal_source=ksrc, macro_source=msrc, post_macros=a["nut"],
               moods=moods, best_time=r["best_time_to_cook"], tags=tags,
               image=r["image"] if meal_ok else None, youtube=r["youtube"] if meal_ok else None,
               mealdb=a["meal"] if r["recipe_source"] == "themealdb" else None, recipe_source=r["recipe_source"], saved=r["saved_count"],
               fact=FACTS.get(rid, "") if status in ("rewritten",) or rid in FACTS else "")
    rec["origin"] = origin_for(rid, name, rec["cuisine"]); rec["origin_plan"] = None if rid in ORIG else plan_origin(rid, name, rec["cuisine"])
    if rec["status"] == "missing" and r["recipe_source"] == "themealdb":
        # times/calories were copied from the unrelated TheMealDB placeholder, so they say nothing about this dish
        rec["total"] = None; rec["time_source"] = None; rec["nutrition"] = None; rec["kcal_source"] = None; rec["macro_source"] = None; rec["difficulty"] = "—"
        rec["tags"] = tags_for(rec["name"], [], [], None, None, None, rec["category"]); rec["moods"] = moods_for(rec["name"], rec["category"], None, rec["tags"], "")
        rec["ingredients"] = []; rec["steps"] = []; rec["servings"] = None
    if rec["status"] == "repo-prev" and rec["time_source"] == "from post":
        rec["time_source"] = "estimated"  # the repo's time now belongs to the different post its current steps came from
    out.append(rec)
assert len({o["id"] for o in out}) == len(out) == len(A)
json.dump({"source": "github.com/poojithmalla8/cooking_recipe data/recipes-*.json", "count": len(out), "recipes": out}, open("recipes.json", "w"), ensure_ascii=False, separators=(",", ":"))
import collections
print(len(out), collections.Counter(o["status"] for o in out), collections.Counter(o["category"] for o in out))
