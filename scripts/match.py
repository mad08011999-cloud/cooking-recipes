import re
STOP={"recipe","style","easy","the","with","and","homemade","best","my","a","of","in","quick","simple","healthy","special","restaurant","indian","street","famous","perfect","ultimate","classic","&","+","s"}
SYN={"chili":"chilli","chillies":"chilli","chilies":"chilli","potato":"potatoes","wings":"wing","eggs":"egg","noodle":"noodles","prawns":"prawn","tacos":"taco","cakes":"cake","rolls":"roll","cookies":"cookie","sandwiches":"sandwich","katsu":"katsu","tikka":"tikka"}
def toks(s):
    w=re.findall(r"[a-z0-9]+",s.lower().replace("’","'").replace("'s",""))
    return [SYN.get(x,x) for x in w if x not in STOP]
def matches(dish,meal):
    d=set(toks(dish)); m=set(toks(meal))
    if not d: return False
    return d<=m
