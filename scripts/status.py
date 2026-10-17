import json, glob, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from clean import clean_ing, clean_steps, key_conflict, parse_macros
from match import matches
M = json.load(open(os.path.join(os.path.dirname(__file__), "themealdb_index.json")))
OK_OVERRIDE = {"general-tso-s-chicken", "chick-fil-a-s-chicken-sandwich", "chicken-shawarma", "tandoori-chicken-rice", "tandoori-chicken-and-rice",
               "chicken-pad-thai", "ramadan-special-chicken-mandi", "and-flavourful-matar-paneer", "unique-matar-paneer"}
BAD_OVERRIDE = {"fried-chicken", "tacos", "pork", "flavorful-dinner"}
FORCE_FLAG = {"noodles": "ingredients are for a chicken ramen, steps are for fried Maggi buns",
              "mixture": "steps are for fettuccine Alfredo, ingredients are for a papad paneer curry",
              "full-recipe": "steps are for shrimp rice-paper bites, ingredients are for a panko chicken rice bowl",
              "coriander-chutney": "steps are for a tandoori sandwich / skewers, ingredients are for paneer potato cutlets"}
SERVE = {"rice", "naan", "roti", "paratha", "bread"}
def assess(r):
    ing, nut = clean_ing(r["ingredients"]); st = clean_steps(r["steps"])
    real = [x for x in ing if not x[2]]
    meal = M.get(r["image"] or "", {}).get("name")
    info = dict(ing=ing, steps=st, nut=nut, macros=parse_macros(nut), meal=meal, why="")
    if r["recipe_source"] == "themealdb":
        ok = (r["id"] in OK_OVERRIDE or matches(r["name"], meal or "")) and r["id"] not in BAD_OVERRIDE
        if not ok:
            info.update(status="missing", why=f"the repo linked this dish to TheMealDB’s “{meal}”, a different dish")
        else:
            info.update(status="repo" if len(st) >= 2 else "partial", why="" if len(st) >= 2 else "only one step in the source")
        return info
    fp, fb = key_conflict(r["name"], ing, st)
    fb2 = [b for b in fb if b not in SERVE]
    why = FORCE_FLAG.get(r["id"]) or (f"steps mention {', '.join(fp + fb2)} which aren’t in the ingredient list" if (fp or len(fb2) >= 3) else "")
    if len(real) >= 2 and len(st) >= 2:
        info.update(status="check" if why else "repo", why=why)
    elif real or st:
        miss = "steps" if len(st) < 2 else "ingredients"
        info.update(status="partial", why=f"the repo has no {miss}" if (len(st) == 0 or len(real) == 0) else f"the repo has very few {miss}")
    else:
        info.update(status="missing", why="the repo has no ingredients or steps for this dish")
    return info
