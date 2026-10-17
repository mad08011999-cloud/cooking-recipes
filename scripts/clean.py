import re
NUT_RE=re.compile(r"(\bkcal\b|\bcal(ories)?\b|\bprotein\b|\bcarbs?\b|\bfat\b|\b\d+\s*g\s*[PCF]\b)",re.I)
def parse_macros(lines):
    out={}
    for l in lines:
        t=l.lower()
        for key,pat in [("kcal",r"(\d{2,4})\s*(?:kcal|cal(?:ories)?)"),("protein",r"(?:protein[:\s~]*(\d+)\s*g|(\d+)\s*g\s*(?:of\s*)?(?:protein|p\b))"),
                        ("carbs",r"(?:carbs?[:\s~]*(\d+)\s*g|(\d+)\s*g\s*(?:carbs?|c\b))"),("fat",r"(?:fat[:\s~]*(\d+)\s*g|(\d+)\s*g\s*(?:fat|f\b))")]:
            m=re.search(pat,t)
            if m and key not in out:
                v=next(g for g in m.groups() if g); out[key]=int(v)
    return out
NUT2=re.compile(r"(\d+\s*g\s*(of\s*)?(protein|carbs?|fat|p|c|f)\b|\b(protein|carbs?|fat|calories|kcal)\s*[:~\-]\s*~?\d|\d+\s*(kcal|calories|cal)\b)",re.I)
def is_nut_line(item):
    t=item.strip()
    return bool(NUT2.search(t)) and len(re.findall(r"[a-z]{4,}",re.sub(r"protein|calories|carbs|kcal|with|per|serving|macros|total",""," "+t.lower())))<=1
def is_header(item):
    t=item.strip()
    return t.endswith(":") or t.lower() in ("slurry","for the sauce","sauce","marinade","ingredients")
def clean_ing(ings):
    out=[];nut=[]
    for i in ings:
        q=(i.get("measure") or "").strip(); it=(i.get("item") or "").strip()
        full=(q+" "+it).strip()
        if not full: continue
        if is_nut_line(full): nut.append(full); continue
        if is_header(it) and not q: out.append(["", it.rstrip(":").strip()+":", True]); continue
        if re.search(r"(dm me|follow|comment|click|link in bio|let me know)",full,re.I): continue
        out.append([q,it,False])
    # exact dupes
    seen=set();res=[]
    for q,it,h in out:
        k=(q.lower(),it.lower())
        if k in seen and not h: continue
        seen.add(k);res.append([q,it,h])
    return res,nut
JUNK_STEP=re.compile(r"^\s*[\[{#]|#\w+|follow|comment\s+[\"“']?\w|link in bio|save this|share this",re.I)
def norm(s): return re.sub(r"[^a-z0-9]+"," ",s.lower()).strip()
def clean_steps(steps):
    s=[]
    for x in steps:
        x=re.sub(r"\s*\[[^\]]*$","",x).strip()           # trailing [ tag list
        x=re.sub(r"\s*\{[^}]*\}\s*","",x).strip()
        x=re.sub(r"\s+"," ",x)
        if not x or JUNK_STEP.search(x) and len(x)<120: continue
        if x.count(",")>=4 and "." not in x and x.islower(): continue
        s.append(x)
    # drop steps that are substrings of another (dupes from split variants)
    n=[norm(x) for x in s]; keep=[]
    for i,x in enumerate(s):
        if any(j!=i and n[i] and n[i] in n[j] and (len(n[j])>len(n[i]) or j<i) for j in range(len(s))): continue
        keep.append(x)
    return keep

def parse_macros(lines):
    t=" | ".join(lines).lower(); out={}
    num=r"(\d+(?:\.\d+)?)"
    pats={"kcal":[num+r"\s*(?:kcal|calories|cals?)\b"],
          "protein":[r"protein\s*[:\-~]*\s*~?"+num+r"\s*g",num+r"\s*g\s*(?:of\s*)?(?:protein|p)\b"],
          "carbs":[r"carbs?\s*[:\-~]*\s*~?"+num+r"\s*g",num+r"\s*g\s*(?:carbs?|c)\b"],
          "fat":[r"fat\s*[:\-~]*\s*~?"+num+r"\s*g",num+r"\s*g\s*(?:fat|f)\b"]}
    for k,ps in pats.items():
        for p in ps:
            m=re.search(p,t)
            if m: out[k]=round(float(m.group(1))); break
    return out
GENERIC=set("""water salt pepper black white oil heat pan pot bowl sauce minutes mins minute medium high low flame cook cooked cooking add mix stir serve
garnish fresh hot cold until golden brown well together little some remaining mixture taste side sides piece pieces large small half cup cups spoon
tablespoon teaspoon tbsp tsp keep aside place make made then once over into from with your this that will them they each about more less needed
optional chopped sliced finely diced minced crushed grated cut boil boiled fry fried bake baked grill air fryer oven tray plate enjoy done dish recipe
butter garlic onion onions ginger chilli chili green red powder paste seeds leaves coriander cilantro lemon lime juice sugar honey flour cornflour cornstarch
spring masala spices spice turmeric cumin garam ghee curd yogurt yoghurt cream milk tomato tomatoes rice""".split())
def words(s): return set(w for w in re.findall(r"[a-z]{4,}",s.lower()))
def foreign_words(name,ings,steps,vocab):
    W=words(name+" "+" ".join(q+" "+i for q,i,*_ in ings))
    Wst={w.rstrip("s") for w in W}
    S=words(" ".join(steps))&vocab
    return sorted(w for w in S-GENERIC if w not in W and w.rstrip("s") not in Wst and w+"s" not in W)

PROT={"shrimp","prawn","chicken","beef","pork","lamb","mutton","fish","salmon","paneer","tofu","soya","bacon","sausage","turkey","lobster","crab","tuna","cod"}
BASE={"fettuccine","pasta","spaghetti","penne","linguine","parmesan","maggi","ramen","noodles","tortilla","tortillas","naan","roti","paratha","bread","buns","bun","potato","potatoes","cauliflower","mushroom","mushrooms","broccoli","cabbage","cornflakes","oats","chocolate","cocoa","dough","rice","quinoa","lentils","dal","chickpeas","beans","avocado","cheese","mozzarella","mayonnaise","mayo","skewers","papad","papads","egg","eggs"}
def wset(s): return {w.rstrip("s") if w not in("chickpeas",) else w for w in re.findall(r"[a-z]+",s.lower())}
def key_conflict(name,ings,steps):
    W=wset(name+" "+" ".join(q+" "+i for q,i,*_ in ings))
    S=wset(" ".join(steps))
    fp=sorted({w for w in S if w in {p.rstrip("s") for p in PROT}}-W)
    fb=sorted({w for w in S if w in {b.rstrip("s") for b in BASE}}-W)
    return fp,fb
