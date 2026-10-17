# Curated recipe data. mode: repo = repo recipe kept (lightly cleaned);
# completed = repo recipe kept, missing quantities/steps filled in;
# rewritten = repo entry was empty or a mismatched placeholder, so a recipe matching the dish name was written.
R = {}
def r(id, name, cat, cuisine, tags, serv, diff, prep, cook, extra, nut, moods, mode, ing, steps, note="", fact=""):
    R[id] = dict(id=id, name=name, category=cat, cuisine=cuisine, tags=tags, servings=serv, difficulty=diff,
                 prep=prep, cook=cook, extra=extra, nutrition=dict(zip(["kcal","protein","carbs","fat","fiber"], nut)),
                 moods=moods, mode=mode,
                 ingredients=[[p.strip() for p in l.split("|",1)] for l in ing.strip().split("\n")] if ing else None,
                 steps=steps, note=note, fact=fact)

r("chicken","Chicken Basquaise (Basque Chicken & Rice)","Main Course","French",["Non-veg","One-pot","Gluten-free"],6,"Medium",20,70,"",(650,48,45,30,4),["weekend","party","rainy"],"repo",None,None,
  "The repo’s ‘Chicken’ entry is TheMealDB’s Chicken Basquaise; kept as-is.","Named after the Basque Country, where Espelette peppers are grown and dried on house façades.")
r("paneer","Matar Paneer","Main Course","Indian",["Vegetarian","Gluten-free"],2,"Easy",10,20,"",(480,22,24,32,7),["weeknight","rainy"],"repo",None,None,"From TheMealDB via the repo.","")
r("butter-chicken","Butter Chicken (Murgh Makhani)","Main Course","Indian",["Non-veg","Gluten-free","Creamy"],4,"Medium",20,35,"+ 1 h marinating",(520,36,14,36,3),["rainy","party","weekend"],"rewritten",
"""600 g | boneless chicken thighs, cubed
150 g | thick yogurt (curd)
1 tbsp | ginger-garlic paste
1½ tsp | Kashmiri red chilli powder
1 tsp | garam masala
1 tbsp | lemon juice
3 tbsp | butter
1 tbsp | oil
1 | onion, finely chopped (optional)
400 g | tomato purée (or 4 ripe tomatoes, blended)
10 | cashews, soaked and blended to a paste
1 tsp | dried fenugreek leaves (kasuri methi)
1 tsp | sugar or honey
100 ml | fresh cream
to taste | salt
handful | fresh coriander""",
["Marinate the chicken with yogurt, ginger-garlic paste, 1 tsp chilli powder, ½ tsp garam masala, lemon juice and salt for at least 1 hour.",
 "Sear or grill the chicken in 1 tbsp oil on high heat until charred at the edges (it can finish cooking in the sauce). Set aside.",
 "In the same pan melt 2 tbsp butter, soften the onion (if using), then add the remaining chilli powder and tomato purée. Simmer 12–15 minutes until thick and the butter separates.",
 "Stir in the cashew paste and a splash of water; simmer 5 minutes. Blend the sauce smooth for a restaurant-style finish.",
 "Add the chicken, sugar and remaining garam masala; simmer 8–10 minutes until the chicken is cooked through.",
 "Crush in the kasuri methi, stir in the cream and last tbsp butter. Garnish with coriander and serve with naan or jeera rice."],
"Repo entry pointed at an unrelated French chicken recipe, so a classic butter chicken recipe is shown.","Created at Moti Mahal restaurant in Delhi in the mid-20th century; a fixture of Punjabi dhaba and wedding menus.")
r("chocolate","Chocolate Alfajores (Dulce de Leche Cookies)","Dessert","Uruguayan",["Vegetarian","Baking"],20,"Medium",40,25,"+ 30 min chilling",(260,3,32,14,1),["sweet","weekend","festive"],"repo",None,None,
  "Repo ‘Chocolate’ entry = TheMealDB chocolate alfajores; makes ~20 sandwich cookies (servings = cookies).","")
r("chilli-chicken","Chilli Chicken (Indo-Chinese)","Entree","Indo-Chinese",["Non-veg","Spicy"],3,"Medium",15,20,"+ 15 min marinating",(420,32,22,22,2),["movie","rainy","latenight"],"rewritten",
"""500 g | boneless chicken, bite-size pieces
1 | egg
3 tbsp | cornflour
1 tbsp | all-purpose flour (maida)
1 tbsp | light soy sauce
1 tsp | ginger-garlic paste
½ tsp | black pepper
oil | for frying
1 tbsp | chopped garlic
1 tbsp | chopped ginger
3 | green chillies, slit
1 | onion, cubed
1 | green capsicum, cubed
1 tbsp | dark soy sauce
2 tbsp | red chilli sauce
1 tbsp | tomato ketchup
1 tsp | vinegar
2 | spring onions, chopped""",
["Mix chicken with egg, 2 tbsp cornflour, maida, light soy sauce, ginger-garlic paste, pepper and salt. Rest 15 minutes.",
 "Deep-fry (or air-fry at 200°C for 12 minutes) until golden and crisp. Drain.",
 "Heat 2 tbsp oil in a wok on high; stir-fry garlic, ginger and green chillies for 30 seconds.",
 "Add onion and capsicum; toss 1–2 minutes so they stay crunchy.",
 "Add dark soy, chilli sauce, ketchup and vinegar. For a gravy version add 1 tbsp cornflour mixed in ½ cup water and simmer until glossy.",
 "Toss in the fried chicken, finish with spring onions and serve hot with fried rice or noodles."],
"Repo entry pointed at an unrelated French chicken recipe; rewritten as classic Indo-Chinese chilli chicken.","A Hakka-Chinese creation from Kolkata, now on almost every Indo-Chinese menu in India.")
r("sandwich","Chivito (Uruguayan Steak Sandwich)","Main Course","Uruguayan",["Non-veg","Baking"],8,"Hard",60,45,"+ overnight dough rest",(780,45,52,42,3),["weekend","party"],"repo",None,None,"TheMealDB chivito with homemade brioche buns.","Chivito is often called Uruguay’s national dish.")
r("chicken-curry","Chicken Katsu Curry","Main Course","Japanese",["Non-veg","Comfort"],4,"Medium",15,30,"",(650,40,55,28,4),["rainy","weeknight"],"repo",None,None,"TheMealDB katsu curry (repo: ‘Chicken Curry’). Serve with rice.","")
r("fried-chicken","Crispy Fried Chicken","Main Course","American",["Non-veg","Comfort"],4,"Medium",20,25,"+ 2 h buttermilk soak",(620,42,28,38,1),["movie","weekend","party"],"rewritten",
"""1 kg | bone-in chicken pieces (drumsticks & thighs)
500 ml | buttermilk (or 450 ml milk + 2 tbsp lemon juice)
1 tbsp | hot sauce
200 g | all-purpose flour
2 tbsp | cornflour
2 tsp | paprika
1 tsp | garlic powder
1 tsp | onion powder
½ tsp | cayenne
2 tsp | salt
1 tsp | black pepper
oil | for deep frying""",
["Soak the chicken in buttermilk, hot sauce and 1 tsp salt for 2 hours (or overnight in the fridge).",
 "Whisk flour, cornflour, spices, remaining salt and pepper in a wide bowl.",
 "Lift chicken from the buttermilk, dredge in flour, dip back in buttermilk briefly and dredge again for extra crags.",
 "Heat oil to 170°C. Fry 3–4 pieces at a time for 12–15 minutes, turning, until deep golden and 75°C inside.",
 "Rest on a rack for 5 minutes. Serve with coleslaw, fries or biscuits."],
"Repo entry pointed at a Chinese fried rice recipe; rewritten as fried chicken.","")
r("chicken-65","Chicken 65","Entree","Indian (Tamil Nadu)",["Non-veg","Spicy","Gluten-free"],4,"Easy",15,20,"+ 30 min marinating",(380,30,12,24,1),["movie","rainy","party"],"rewritten",
"""500 g | boneless chicken, cubed
1 tbsp | ginger-garlic paste
1½ tsp | Kashmiri chilli powder
½ tsp | turmeric
½ tsp | black pepper
½ tsp | garam masala
1 tbsp | lemon juice
2 tbsp | yogurt
3 tbsp | cornflour
1 tbsp | rice flour
1 | egg white
oil | for frying
1 sprig | curry leaves
3 | green chillies, slit
1 tsp | chopped garlic""",
["Mix chicken with ginger-garlic paste, chilli powder, turmeric, pepper, garam masala, lemon juice, yogurt and salt. Marinate 30 minutes.",
 "Add cornflour, rice flour and egg white; mix to coat each piece.",
 "Deep-fry in batches at 175°C for 5–6 minutes until crisp and red-golden.",
 "In 1 tbsp hot oil, crackle the curry leaves, green chillies and garlic; toss the fried chicken through.",
 "Serve hot with onion rings and lemon wedges."],
"Repo entry pointed at an unrelated French chicken recipe; rewritten as Chicken 65.","Credited to Hotel Buhari in Chennai (1965 is the most cited story for the name).")
r("chicken-tikka","Chicken Tikka","Entree","Indian (Punjabi)",["Non-veg","High-protein","Gluten-free"],4,"Easy",15,15,"+ 2 h marinating",(290,38,6,12,1),["party","gym","weekend"],"rewritten",
"""600 g | boneless chicken thighs, 4 cm cubes
150 g | thick (hung) yogurt
1 tbsp | ginger-garlic paste
1½ tsp | Kashmiri chilli powder
1 tsp | ground cumin
1 tsp | garam masala
½ tsp | turmeric
1 tbsp | mustard oil (or any oil)
1 tbsp | lemon juice
1 tsp | kasuri methi
1 | onion & 1 capsicum, cut into chunks (optional)
1 tbsp | melted butter for basting
1 tsp | chaat masala to finish""",
["Whisk yogurt with ginger-garlic paste, spices, oil, lemon juice, kasuri methi and salt.",
 "Coat the chicken (and veg, if using) and marinate 2 hours or overnight.",
 "Thread onto skewers. Grill, broil or bake at 240°C for 12–15 minutes, turning once and basting with butter, until charred at the edges.",
 "Sprinkle chaat masala and serve with mint chutney and sliced onions."],
"Repo entry pointed at an unrelated French chicken recipe; rewritten as chicken tikka.","")
r("potatoes","Maple Bacon Breakfast Potatoes","Breakfast","Canadian",["Non-veg","Gluten-free"],2,"Easy",10,20,"",(330,8,42,15,4),["brunch","weekend"],"repo",None,None,"TheMealDB breakfast potatoes.","")
r("biryani","Lamb Biryani","Main Course","Indian",["Non-veg","Celebration"],4,"Hard",40,90,"+ 20 min soaking",(720,35,78,28,3),["festive","weekend","party"],"completed",None,None,
  "Repo/TheMealDB steps stopped before layering the rice; the final steps were added (marked).","Biryani is a staple of Eid feasts and Indian weddings.")
r("chicken-fried-rice","Chicken Fried Rice","Main Course","Chinese",["Non-veg","Quick","Meal prep"],4,"Easy",15,15,"(use day-old rice)",(520,30,62,16,3),["weeknight","mealprep","latenight"],"completed",None,None,
  "Repo/TheMealDB steps stopped after browning the chicken; the remaining steps were added (marked).","")
r("tandoori-chicken","Tandoori Chicken","Main Course","Indian",["Non-veg","High-protein","Gluten-free"],8,"Easy",15,20,"+ 1 h marinating",(360,44,8,16,1),["party","weekend","gym"],"repo",None,None,"TheMealDB tandoori chicken (16 thighs, serves ~8).","")
r("egg-fried-rice","Egg Fried Rice","Main Course","Chinese",["Eggetarian","Quick","Budget"],2,"Easy",10,10,"",(450,15,62,16,3),["weeknight","latenight"],"rewritten",
"""3 cups | cooked rice, preferably day-old
3 | eggs, beaten
2 tbsp | oil
3 | garlic cloves, minced
½ cup | peas & diced carrots
3 | spring onions (whites and greens separated)
1½ tbsp | light soy sauce
1 tsp | dark soy sauce (for colour)
½ tsp | white pepper
1 tsp | sesame oil""",
["Break up the rice with your fingers so no clumps remain.",
 "Heat 1 tbsp oil in a wok on high; scramble the eggs until just set, then push aside or remove.",
 "Add remaining oil, garlic and spring-onion whites for 30 seconds, then peas and carrots for 1 minute.",
 "Add the rice; toss for 2–3 minutes until hot and slightly toasty.",
 "Season with both soy sauces and white pepper, fold the egg back in, finish with sesame oil and spring-onion greens."],
"Repo entry reused a chicken fried rice recipe; rewritten as an egg fried rice.","")
r("manchurian","Veg Manchurian Noodle Frankie","Entree","Indo-Chinese",["Vegetarian","Street food"],4,"Medium",30,30,"",(560,12,78,22,5),["movie","latenight","weekend"],"completed",
"""1 cup | finely shredded cabbage (for balls)
1 | onion, finely chopped
1 tsp | salt
½ tsp | black pepper
1 cup | refined flour (maida) for balls
oil | for deep frying
2 tbsp | oil (for the sauce)
5–6 | garlic cloves, chopped
½ | onion, diced
⅓ cup | capsicum, diced
2 tbsp | Schezwan sauce (+ extra for spreading)
1 tsp | soy sauce
2 tbsp | red chilli sauce
2 cups | refined flour (maida) for the rotis
½ tsp | salt (roti dough)
2 tsp | oil (roti dough)
¾ cup | water
1 pack (150 g) | noodles, boiled
1 tbsp | butter
½ cup | shredded cabbage to top""",
None,"From the repo (Instagram caption). Quantities came from the caption steps.","")
r("full-recipe","Crispy Five-Spice Chicken (Air Fryer)","Entree","Chinese",["Non-veg","Air fryer","High-protein"],3,"Easy",15,15,"+ 20 min marinating",(330,32,24,10,1),["gym","weeknight","movie"],"completed",
"""1 lb (450 g) | skinless, boneless chicken thighs, bite-size
½ tsp | white pepper
1 tsp | Chinese five-spice powder
1½ tbsp | minced garlic
1 tbsp | minced ginger
1 tbsp | Shaoxing wine
2 tbsp | soy sauce
¾ cup | coarse potato starch
1 | egg white
1 second | spray of cooking oil""",
["Mix the chicken with white pepper, five-spice, garlic, ginger, Shaoxing wine and soy sauce. Marinate 20 minutes (★ step added).",
 "Stir in the egg white until every piece is coated (★).",
 "Toss the pieces in the coarse potato starch, pressing so it sticks; rest 5 minutes so the coating hydrates (★).",
 "Arrange in a single layer in the air-fryer basket and spray lightly with oil (★).",
 "Air-fry at 200°C / 400°F for 12–15 minutes, shaking halfway, until crisp and cooked through (★)."],
"Repo title was literally ‘⇩ Full Recipe ⇩’ with ingredients only; renamed from its ingredients and steps were written (★).","")
r("chicken-biryani","Hyderabadi Chicken Biryani","Main Course","Indian (Hyderabadi)",["Non-veg","Celebration","Gluten-free"],5,"Hard",30,60,"+ 2 h marinating",(680,36,80,22,3),["festive","weekend","party"],"rewritten",
"""750 g | bone-in chicken
2½ cups | aged basmati rice, soaked 30 min
250 g | yogurt
1½ tbsp | ginger-garlic paste
2 tsp | red chilli powder
½ tsp | turmeric
1½ tsp | biryani masala / garam masala
3 | onions, thinly sliced & fried golden (birista)
handful each | mint & coriander leaves
3 | green chillies, slit
1 | lemon, juiced
3 tbsp | ghee
pinch | saffron soaked in 3 tbsp warm milk
whole spices | 2 bay leaves, 4 green cardamom, 4 cloves, 1 cinnamon stick, 1 tsp shahi jeera""",
["Marinate chicken with yogurt, ginger-garlic paste, chilli, turmeric, biryani masala, half the fried onions, half the herbs, green chillies, lemon juice, 1 tbsp ghee and salt for 2 hours.",
 "Spread the marinated chicken in a heavy-bottomed pot.",
 "Boil plenty of salted water with the whole spices; cook the rice until 70% done (about 5 minutes). Drain.",
 "Layer the rice over the chicken. Top with remaining fried onions, herbs, saffron milk and 2 tbsp ghee.",
 "Seal the pot with a lid (and dough or foil). Cook on high 5 minutes, then the lowest heat for 35–40 minutes (dum).",
 "Rest 10 minutes, then gently mix from the side. Serve with raita and mirchi ka salan."],
"Repo entry pointed at an unrelated French chicken recipe; rewritten as kacchi-style Hyderabadi chicken biryani.","Hyderabadi biryani grew out of the Nizams’ royal kitchens and is central to weddings and Eid in the city.")
r("chicken-manchurian","Chicken Manchurian (Gravy)","Main Course","Indo-Chinese",["Non-veg","Spicy"],3,"Medium",15,25,"",(430,30,24,24,2),["rainy","weeknight","latenight"],"rewritten",
"""400 g | boneless chicken, small cubes
1 | egg
3 tbsp | cornflour (+1 tbsp for gravy)
1 tbsp | maida
1 tsp | ginger-garlic paste
1 tbsp | soy sauce (+1 tbsp for gravy)
oil | for frying
1 tbsp each | chopped garlic & ginger
2 | green chillies, chopped
1 | onion, diced
½ | capsicum, diced
1 tbsp | red chilli sauce
1 tbsp | tomato ketchup
1 tsp | vinegar
1 cup | water or stock
3 | spring onions, chopped""",
["Coat the chicken with egg, 3 tbsp cornflour, maida, ginger-garlic paste, 1 tbsp soy sauce and salt.",
 "Deep-fry until crisp and golden; drain.",
 "In a wok, sauté garlic, ginger and chillies on high heat for 30 seconds; add onion and capsicum for 1 minute.",
 "Add soy sauce, chilli sauce, ketchup and vinegar, then the water. Bring to a boil.",
 "Thicken with 1 tbsp cornflour mixed in 3 tbsp water until glossy.",
 "Add the chicken, toss, top with spring onions and serve with fried rice."],
"Repo entry pointed at an unrelated French chicken recipe; rewritten as chicken Manchurian.","Manchurian is usually credited to chef Nelson Wang in Mumbai in the 1970s; it isn’t from Manchuria at all.")
r("garlic-chicken","Garlic Chicken (Pollo al Ajillo)","Main Course","Spanish",["Non-veg","Gluten-free","One-pan"],4,"Easy",10,30,"",(420,38,4,26,0),["weeknight","party"],"rewritten",
"""1 kg | chicken thighs/drumsticks, bone-in, cut small
1 head | garlic (about 12 cloves), lightly crushed
4 tbsp | olive oil
2 | bay leaves
1 tsp | smoked paprika (optional)
120 ml | dry white wine or sherry
120 ml | chicken stock
2 tbsp | chopped parsley
to taste | salt & pepper""",
["Season the chicken well with salt and pepper.",
 "Fry the garlic cloves gently in olive oil until golden; remove and keep.",
 "Brown the chicken in the garlicky oil on all sides, 10–12 minutes.",
 "Add bay leaves, paprika and wine; let it bubble 2 minutes, then add stock and the garlic back in.",
 "Cover and simmer 15 minutes until cooked through; uncover to reduce to a glossy sauce.",
 "Finish with parsley and serve with crusty bread or rice."],
"Repo entry pointed at an unrelated French chicken recipe; rewritten as a Spanish-style garlic chicken.","")
r("korean-popcorn-chicken","Korean Popcorn Chicken (Air Fryer)","Snack","Korean",["Non-veg","Air fryer","High-protein","Sweet & spicy"],2,"Easy",15,20,"",(450,42,48,8,2),["gym","weeknight","movie"],"completed",
"""1 medium (250 g) | chicken breast, bite-size
1 | egg, beaten
60 g | cornflakes, crushed
½ tbsp | paprika
½ tbsp | chilli powder
½ tbsp | garlic powder
½ tbsp | ground ginger
5 tbsp | gochujang (sauce)
1 tbsp | soy sauce
1 tsp | rice wine vinegar
1 tsp | mirin
1 tbsp | honey
to garnish | sesame seeds & spring onion""",
["Cut the chicken breast into bite-size pieces.",
 "Coat the chicken in the paprika, chilli, garlic powder and ground ginger.",
 "Dip in the egg, then immediately coat in crushed cornflakes.",
 "Air-fry for 16 minutes (about 190°C), flipping halfway.",
 "While cooking, combine the gochujang, soy sauce, vinegar, mirin and honey.",
 "Heat and slightly reduce the sauce, add the chicken and toss to coat.",
 "Garnish with sesame and spring onion."],
"From the repo (Instagram caption); quantities for spices/cornflakes estimated from the caption’s ‘one medium breast’ note.","")
r("mixture","Stuffed Papad Paneer Curry","Main Course","Indian (Rajasthani-style)",["Vegetarian","Gluten-free"],3,"Medium",20,25,"",(410,15,24,28,4),["rainy","weekend"],"completed",
"""5 | tomatoes, chopped
2 | onions, chopped
5–6 | garlic cloves
½ inch | ginger
100 g | paneer, grated (+2 tbsp to garnish)
2 tbsp | coriander, chopped
2 tbsp | mixed dry fruits, chopped
2 | green chillies
2 tsp | Kashmiri red chilli powder
½ tsp | garam masala
½ tsp + ½ tsp | turmeric powder
¼ tsp + 1 tsp | salt
6 | papads
2 tbsp + for frying | oil
2 | bay leaves
1 | star anise
1 inch | cinnamon
1 tsp | fennel seeds
1 tsp | cumin seeds
1 tsp | red chilli powder
½ cup | water
3 tbsp | fresh cream""",
None,"Repo name was just ‘Mixture’; renamed from its steps. Quantities came from the caption steps.","Papad ki sabzi (papad curry) is a classic of desert-state Rajasthan, where fresh vegetables were historically scarce.")
r("paneer-tikka","Paneer Tikka","Entree","Indian (Punjabi)",["Vegetarian","Gluten-free","High-protein"],3,"Easy",15,15,"+ 30 min marinating",(340,18,10,26,2),["party","weekend","movie"],"rewritten",
"""300 g | paneer, 3 cm cubes
1 | onion, petals
1 | capsicum, chunks
120 g | hung curd (thick yogurt)
1 tbsp | gram flour (besan), roasted
1 tbsp | mustard oil
1 tsp | ginger-garlic paste
1½ tsp | Kashmiri chilli powder
½ tsp | turmeric
1 tsp | garam masala
1 tsp | kasuri methi
1 tbsp | lemon juice
1 tsp | chaat masala""",
["Whisk curd, besan, mustard oil, ginger-garlic paste, spices, kasuri methi, lemon juice and salt into a thick marinade.",
 "Fold in paneer, onion and capsicum; marinate 30 minutes.",
 "Thread onto skewers and grill/air-fry at 220°C for 10–12 minutes, or cook on a hot tawa, until charred at the edges.",
 "Sprinkle chaat masala; serve with mint chutney."],
"Repo entry reused a matar paneer recipe; rewritten as paneer tikka.","")
r("bang-bang-chicken","Bang Bang Chicken","Entree","Chinese-American fusion",["Non-veg","Spicy","Creamy"],3,"Easy",15,15,"",(480,30,26,28,1),["movie","party","latenight"],"rewritten",
"""450 g | chicken breast, bite-size
1 | egg
½ cup | cornflour
¼ cup | all-purpose flour
oil | for frying
½ cup | mayonnaise
3 tbsp | sweet chilli sauce
1–2 tsp | sriracha
1 tsp | honey
1 tsp | rice vinegar
2 | spring onions, sliced""",
["Season chicken with salt and pepper, dip in beaten egg, then toss in the cornflour-flour mix.",
 "Deep- or air-fry until crisp and golden (about 6 minutes in oil at 175°C or 12 minutes at 200°C in an air fryer).",
 "Whisk mayo, sweet chilli, sriracha, honey and vinegar into the bang bang sauce.",
 "Toss the hot chicken in the sauce, scatter spring onions and serve over lettuce or rice."],
"Repo entry pointed at an unrelated French chicken recipe; rewritten in the popular creamy-sweet-chilli style.","The original Sichuan bang bang chicken is a cold shredded dish; the creamy fried version is a modern restaurant twist.")
r("butter-garlic-chicken","Butter Garlic Chicken","Main Course","Indian-Chinese fusion",["Non-veg","Quick","Gluten-free"],3,"Easy",10,15,"",(380,34,4,25,0),["weeknight","gym","latenight"],"rewritten",
"""500 g | boneless chicken, bite-size
½ tsp | black pepper
1 tsp | lemon juice
1 tbsp | cornflour
3 tbsp | butter
12 | garlic cloves, finely chopped
1 tsp | chilli flakes
1 tsp | dried oregano or mixed herbs
2 tbsp | chopped parsley or coriander
to taste | salt""",
["Toss chicken with salt, pepper, lemon juice and cornflour.",
 "Sear in 1 tbsp butter on high heat until golden and cooked through, 6–8 minutes. Remove.",
 "Lower the heat, melt the remaining butter and cook the garlic until fragrant and pale gold (don’t burn).",
 "Add chilli flakes and oregano, return the chicken and toss to glaze.",
 "Finish with herbs and serve hot."],
"Repo entry had no ingredients or steps; recipe written to match the name.","")
r("chicken-fry","Andhra Chicken Fry","Main Course","Indian (Andhra)",["Non-veg","Spicy","Gluten-free"],4,"Medium",15,35,"+ 30 min marinating",(410,34,8,26,2),["weekend","rainy"],"rewritten",
"""750 g | bone-in chicken, curry cut
1 tbsp | ginger-garlic paste
½ tsp | turmeric
1½ tsp | red chilli powder
1 tbsp | lemon juice
3 tbsp | oil
1 | onion, finely sliced
3 | green chillies, slit
2 sprigs | curry leaves
1 tsp | coriander powder
1½ tsp | freshly ground black pepper
1 tsp | garam masala
2 tbsp | chopped coriander""",
["Marinate chicken with ginger-garlic paste, turmeric, chilli powder, lemon juice and salt for 30 minutes.",
 "Heat oil; fry onion, green chillies and curry leaves until golden.",
 "Add the chicken and cook on medium-high 5 minutes, then cover and cook 15 minutes in its own juices.",
 "Uncover, add coriander powder, pepper and garam masala; roast, stirring, until dry and dark-edged, 10–12 minutes.",
 "Garnish with coriander; serve with rice and rasam or chapati."],
"Repo entry pointed at an unrelated French chicken recipe; rewritten as an Andhra-style dry chicken fry.","")
r("chilli-paneer","Chilli Paneer","Entree","Indo-Chinese",["Vegetarian","Spicy"],3,"Easy",15,15,"",(420,18,22,30,2),["movie","rainy","latenight"],"rewritten",
"""250 g | paneer, cubes
3 tbsp | cornflour
2 tbsp | maida
½ tsp | pepper
oil | for frying
1 tbsp each | chopped garlic & ginger
2 | green chillies, slit
1 | onion, cubed
1 | capsicum, cubed
1 tbsp | soy sauce
1½ tbsp | red chilli sauce
1 tbsp | ketchup
1 tsp | vinegar
2 | spring onions""",
["Make a thick batter with cornflour, maida, pepper, salt and water; coat the paneer.",
 "Shallow- or deep-fry until light golden and crisp; drain.",
 "Stir-fry garlic, ginger and chillies on high heat, then onion and capsicum for a minute.",
 "Add sauces and vinegar (plus ½ cup water + 1 tsp cornflour for a gravy version).",
 "Toss in the paneer, finish with spring onions, serve immediately."],
"Repo entry reused a matar paneer recipe; rewritten as chilli paneer.","")
r("coriander-chutney","Chutney Paneer Potato Toastie","Snack","Indian (street-style)",["Vegetarian"],2,"Easy",15,10,"",(480,20,46,24,5),["brunch","weeknight","latenight"],"completed",
"""1 tsp | mustard seeds
1 cup | paneer, grated
½ cup | potato, boiled & grated
½ | red onion, finely diced
1 tsp | spicy garlic crunch seasoning (Kinder’s or similar)
½ tsp each | turmeric, chilli powder & cumin powder
to taste | salt
1 cup | fresh mint & coriander (chutney)
2 + ½ inch | green chillies & ginger (chutney)
squeeze | lemon juice & salt (chutney)
4 | sourdough bread slices
½ cup | grated cheese (Amul or cheddar)
1 tbsp | olive oil or butter for toasting
to dip | tomato sauce + Greek yogurt""",
["Blend the mint, coriander, green chillies, ginger, lemon juice and salt until smooth and bright green.",
 "Crackle mustard seeds in a little oil; add onion, then paneer, potato, the spices, garlic crunch and salt. Mix 2 minutes and cool slightly (★ inferred from ingredient list).",
 "Spread chutney on the sourdough, layer the spicy filling and grated cheese, and close the sandwich.",
 "Toast on medium-low heat with olive oil or butter until golden brown and melted.",
 "Serve with tomato sauce + Greek yogurt dip."],
"Repo name was ‘Coriander Chutney’ and its steps belonged to a different recipe (paneer lollipops); the caption’s own ‘Quick Steps’ for this toastie are used instead.","")
r("fried-rice","Veg Fried Rice (Indo-Chinese)","Main Course","Indo-Chinese",["Vegan","Quick","Budget"],3,"Easy",15,10,"",(400,8,66,12,4),["weeknight","mealprep","latenight"],"rewritten",
"""3 cups | day-old cooked basmati rice
2 tbsp | oil
1 tbsp | chopped garlic
½ cup | carrots, finely diced
½ cup | beans, finely chopped
½ cup | cabbage, shredded
½ | capsicum, diced
3 | spring onions
1½ tbsp | soy sauce
1 tsp | vinegar
½ tsp | black pepper""",
["Heat oil in a wok until smoking; add garlic for 20 seconds.",
 "Add carrots and beans for 2 minutes, then cabbage, capsicum and spring-onion whites for 1 minute.",
 "Add the rice, toss on high heat for 3 minutes.",
 "Season with soy sauce, vinegar, pepper and salt; finish with spring-onion greens."],
"Repo entry duplicated the chicken fried rice recipe; rewritten as a vegetable version.","")
r("noodles","Crispy Maggi Noodle Burger","Snack","Indian (fusion)",["Vegetarian","Street food"],3,"Medium",20,20,"+ 2 h freezing",(560,12,66,28,4),["movie","latenight"],"completed",
"""3 packs | Maggi noodles
3 cups | water
½ tsp | salt
oil | for frying
¼ cup | mayonnaise
1 tbsp | tomato ketchup
1 tbsp | Maggi masala (from the packs)
3 | aloo tikkis (potato patties)
6 | lettuce leaves
1 | tomato, sliced
1 | onion, sliced""",
["Cook 3 packs of Maggi in water with salt until almost dry.",
 "Pour onto a parchment-lined tray, press flat and freeze for 2 hours.",
 "Maggi mayonnaise: mix ketchup and Maggi masala into the mayo.",
 "Cut the Maggi into roundels (bun-sized) and fry until golden brown.",
 "Assemble: Maggi bun, mayo, lettuce, aloo tikki, tomato, onion, Maggi bun."],
"From the repo (caption); quantities for sauces/patties estimated.","Maggi began as a Swiss brand; its instant noodles became an Indian cultural icon from the 1980s.")
r("paneer-bhurji","Paneer Bhurji","Breakfast","Indian (Punjabi)",["Vegetarian","High-protein","Gluten-free","Quick"],2,"Easy",10,10,"",(380,22,12,28,3),["brunch","weeknight","gym"],"rewritten",
"""250 g | paneer, crumbled
1 tbsp | butter or oil
1 tsp | cumin seeds
1 | onion, finely chopped
1 | green chilli, chopped
1 tsp | ginger, grated
1 | tomato, chopped
¼ tsp | turmeric
½ tsp | red chilli powder
½ tsp | garam masala
2 tbsp | milk
2 tbsp | coriander""",
["Heat butter; crackle cumin, then soften onion, green chilli and ginger.",
 "Add tomato, turmeric, chilli powder and salt; cook until jammy, 3–4 minutes.",
 "Add crumbled paneer and milk; toss 2–3 minutes (don’t overcook or it turns rubbery).",
 "Finish with garam masala and coriander. Serve with toast, paratha or pav."],
"Repo entry reused a matar paneer recipe; rewritten as paneer bhurji.","")
r("pasta","White Sauce Pasta","Main Course","Italian (Indian-style)",["Vegetarian","Creamy","Kid-friendly"],3,"Easy",10,20,"",(520,16,64,22,4),["weeknight","rainy"],"completed",
"""200 g | pasta (penne), boiled
2 cups | milk, boiled with ½ onion, 1 tej patta (bay leaf) & 2 cloves
2 tbsp | butter
2 tbsp | maida (flour)
½ | onion, diced
½ | capsicum, diced
¼ cup | sweet corn
1 tsp | chilli flakes
1 tsp | oregano
½ tsp | black pepper
to taste | salt""",
["Infuse the milk: simmer it with onion, tej patta and cloves for 5 minutes, then strain (★ steps written from the ingredient list).",
 "Sauté onion, capsicum and corn in 1 tbsp butter for 2 minutes; set aside (★).",
 "Melt remaining butter, stir in the maida for 1 minute, then whisk in the infused milk until smooth and thick (★).",
 "Season with chilli flakes, oregano, pepper and salt; add veggies and boiled pasta (★).",
 "Toss 1–2 minutes and serve hot (★)."],
"Repo caption listed ingredients only; steps written from them (★).","")
r("salad","Warm Potato, Green Bean & Bacon Salad","Side Dish","European",["Non-veg","Gluten-free"],2,"Easy",15,20,"",(470,17,30,32,6),["weekend","brunch"],"repo",None,None,"TheMealDB potato salad (repo ‘Salad’).","")
r("soya","Crispy Gochujang Soya Chunks (Air Fryer)","Snack","Korean-Indian fusion",["Vegan","High-protein","Air fryer"],2,"Easy",15,20,"",(280,26,28,6,6),["gym","movie","weeknight"],"completed",
"""50 g | big soya chunks
as needed | water
to taste | salt
½ tbsp | ginger-garlic paste
1 tbsp | rice flour
1 tbsp | corn flour
1 tsp | red chilli powder
1 tbsp | soya sauce
1 tsp | oil (for sauce)
½ | onion, chopped
2 | garlic cloves, chopped
1 tbsp | gochujang paste
1 tbsp | chilli tomato ketchup
½ tsp | degi mirch
½ cup | water (sauce)
to garnish | toasted sesame & spring onion""",
None,"From the repo (caption). Sauce ingredients mentioned in steps were added to the ingredient list.","")
r("spring-rolls","Veg Spring Rolls","Entree","Chinese",["Vegan","Party food"],4,"Medium",30,20,"",(320,6,36,16,3),["party","movie","rainy"],"rewritten",
"""12 | spring roll wrappers
2 cups | cabbage, finely shredded
1 | carrot, julienned
½ | capsicum, thin strips
½ cup | bean sprouts or boiled glass noodles
2 | spring onions
1 tbsp | garlic, minced
1 tbsp | soy sauce
½ tsp | black pepper
1 tbsp | cornflour + 2 tbsp water (sealing paste)
oil | for frying""",
["Stir-fry garlic, then all the vegetables on high heat for 2 minutes; season with soy sauce, pepper and salt. Cool completely.",
 "Place 2 tbsp filling on each wrapper, fold the sides in and roll tightly; seal with the cornflour paste.",
 "Deep-fry at 170°C until golden and blistered, 4–5 minutes (or brush with oil and air-fry at 190°C for 10–12 minutes).",
 "Serve with sweet chilli sauce."],
"Repo entry pointed at an unrelated Jamaican plantain-roll recipe; rewritten as veg spring rolls.","Spring rolls are traditionally eaten around the Spring Festival (Chinese New Year), hence the name.")
r("tofu","Crispy Chilli Garlic Tofu","Main Course","Chinese-inspired",["Vegan","High-protein","Quick"],2,"Easy",15,15,"",(360,22,20,22,3),["weeknight","gym"],"rewritten",
"""400 g | firm tofu, pressed & cubed
2 tbsp | cornflour
2 tbsp | oil
4 | garlic cloves, minced
1 tsp | ginger, minced
1 tbsp | chilli crisp or chilli oil
1½ tbsp | soy sauce
1 tsp | maple syrup or sugar
1 tsp | rice vinegar
2 | spring onions
1 tsp | sesame seeds""",
["Press tofu 10 minutes, cube, and toss with cornflour and a pinch of salt.",
 "Pan-fry in oil (or air-fry at 200°C for 15 minutes) until golden on all sides.",
 "In the same pan, sizzle garlic and ginger 30 seconds; add chilli crisp, soy, sweetener and vinegar.",
 "Toss the tofu to glaze; finish with spring onions and sesame. Serve with rice."],
"Repo entry had no ingredients or steps; recipe written to match the name.","")
r("airfryer-chilli-chicken","Air Fryer Chilli Chicken","Entree","Indo-Chinese",["Non-veg","Air fryer","High-protein"],3,"Easy",15,15,"",(340,36,16,14,2),["gym","weeknight","movie"],"completed",
"""500 g | boneless chicken, small pieces
1 | egg
2 tbsp | cornstarch
2 tbsp | maida
1 tsp | pepper powder
1 tbsp | light soy sauce
to taste | salt
1 tbsp | dark soy sauce (sauce)
1 tbsp | oyster sauce (sauce)
1½ tbsp | red chilli sauce (sauce)
1 tbsp | tomato ketchup (sauce)
1 | capsicum, cubed
to garnish | coriander & spring onion greens""",
["Marinate the chicken with salt, egg, cornstarch, maida, pepper powder and light soy sauce. Air-fry in a greased basket at 200°C for 10–14 minutes, flipping halfway, until golden and cooked through.",
 "Mix dark soy sauce, oyster sauce, red chilli sauce and tomato ketchup to prepare the sauce.",
 "In a hot pan, add the sauce, capsicum and the air-fried chicken. Toss on high heat until evenly coated; adjust seasoning and garnish with coriander and spring onion greens."],
"From the repo (caption). Sauce ingredients mentioned in the steps were added; their quantities are estimated.","")
r("amritsar-style-paneer-bhurji","Amritsari Paneer Bhurji (Dhaba Style)","Breakfast","Indian (Punjabi)",["Vegetarian","High-protein","Gluten-free"],3,"Easy",10,15,"",(420,22,14,31,3),["brunch","weekend","rainy"],"rewritten",
"""300 g | paneer, crumbled
2 tbsp | ghee or butter
1 tsp | cumin seeds
2 | onions, finely chopped
1 tbsp | ginger-garlic paste
2 | green chillies
2 | tomatoes, finely chopped
½ tsp | turmeric
1 tsp | Kashmiri chilli powder
1 tsp | coriander powder
1 tsp | Amritsari / chole masala (or garam masala)
1 tsp | kasuri methi
2 tbsp | cream or malai
2 tbsp | coriander""",
["Heat ghee, crackle cumin; cook onions until light brown.",
 "Add ginger-garlic paste and chillies for 1 minute, then tomatoes and all spice powders; cook until oil separates, 5–6 minutes.",
 "Add a splash of water, then the paneer and salt; mix and cook 3 minutes.",
 "Stir in kasuri methi and cream; finish with coriander and an extra knob of butter. Serve with butter-laden pav or parathas."],
"Repo entry had no ingredients or steps; recipe written to match the name.","Amritsar’s dhabas are famous for rich, butter-heavy Punjabi breakfasts.")
r("apollo-fish","Apollo Fish","Entree","Indian (Hyderabadi)",["Pescatarian","Spicy"],3,"Medium",20,20,"+ 20 min marinating",(360,30,14,20,1),["party","weekend","movie"],"rewritten",
"""500 g | boneless white fish (basa, murrel or tilapia), strips
1 tbsp | ginger-garlic paste
1 tsp | red chilli powder
1 | egg
2 tbsp | cornflour
1 tbsp | maida
oil | for frying
1 tbsp | chopped garlic
3 | green chillies, slit
1 sprig | curry leaves
3 tbsp | thick yogurt
1 tbsp | red chilli sauce
1 tsp | soy sauce
½ tsp | sugar
1 tbsp | lemon juice
2 tbsp | coriander""",
["Marinate fish with ginger-garlic paste, chilli powder, salt, egg, cornflour and maida for 20 minutes.",
 "Deep-fry until crisp and golden; drain.",
 "In 1 tbsp oil, sauté garlic, green chillies and curry leaves.",
 "Lower the heat; stir in yogurt, chilli sauce, soy sauce and sugar until it thickens and coats the pan.",
 "Toss the fish through, add lemon juice and coriander, serve hot."],
"Repo entry pointed at an unrelated Jamaican escovitch fish recipe; rewritten as Hyderabadi Apollo fish.","Apollo fish is a Hyderabad restaurant favourite, typically served as a starter.")
r("bang-bang-paneer","Bang Bang Paneer","Entree","Indo-Chinese fusion",["Vegetarian","Creamy","Spicy"],3,"Easy",10,15,"",(470,18,24,34,1),["movie","party"],"rewritten",
"""250 g | paneer, cubes
3 tbsp | cornflour
2 tbsp | maida
½ tsp | chilli powder
oil | for frying
¼ cup | mayonnaise
2 tbsp | sweet chilli sauce
1 tsp | sriracha
1 tsp | honey
2 | spring onions
1 tsp | sesame seeds""",
["Make a batter with cornflour, maida, chilli powder, salt and water; coat paneer.",
 "Fry or air-fry (200°C, 10 minutes) until crisp.",
 "Whisk mayo, sweet chilli, sriracha and honey.",
 "Toss paneer in the sauce; garnish with spring onions and sesame."],
"Repo entry reused a matar paneer recipe; rewritten in bang bang style.","")
r("bread","Bread Omelette","Breakfast","Indian (street food)",["Eggetarian","Quick","Budget"],1,"Easy",5,7,"",(330,16,28,17,2),["brunch","weeknight","latenight"],"completed",
"""2 | bread slices
2 | eggs
½ tsp | salt
1 tbsp | onion, finely chopped (optional)
1 | green chilli, chopped (optional)
1 tbsp | coriander (optional)
pinch | black pepper / chilli powder
1 tsp | butter""",
["Whisk eggs with salt, onion, chilli, coriander and pepper (★ steps written; the repo only said ‘Make and enjoy’).",
 "Melt butter in a pan, pour in the eggs and immediately place both bread slices on top.",
 "When the base sets (about 1 minute), flip the whole thing so the bread toasts.",
 "Fold the overhanging omelette over the bread, fold in half into a sandwich and toast both sides.",
 "Serve with ketchup and a cup of chai."],
"Repo had only ‘2 bread, 2 egg, salt — Make and enjoy’; quantities kept, steps written (★). Optional add-ins are extras.","")
r("caramelized-onion-chicken","Caramelized Onion Herb Chicken (Meal Prep)","Main Course","Mediterranean",["Non-veg","High-protein","Meal prep","Gluten-free"],5,"Easy",15,45,"",(300,44,10,9,2),["mealprep","gym","weeknight"],"completed",
"""1000 g | raw chicken breast, cubed
1.5 tsp | salt
1.5 tsp | black pepper
2 tsp | garlic powder
2 tsp | oregano
2 tsp | smoked paprika
2 tsp | dried basil
3 tsp | olive oil
10 g | reduced-fat butter (for cooking)
3 | large onions, thinly sliced (★ implied by the title)
1 tsp | balsamic vinegar or brown sugar (★ optional)""",
["Slowly cook the onions in the butter and 1 tsp oil over medium-low heat, stirring often, for 25–30 minutes until deep golden (★ steps written).",
 "Meanwhile toss the chicken with salt, pepper, garlic powder, oregano, paprika, basil and remaining olive oil.",
 "Add balsamic to the onions, scrape the pan, then move onions aside.",
 "Turn up the heat and sear the chicken until cooked through, 8–10 minutes.",
 "Fold the onions through. Portion into 5 containers with rice or veg."],
"Repo caption had ingredients only (and no onions, despite the name); steps and onions added (★).","")
r("chicken-65-biryani","Chicken 65 Biryani","Main Course","Indian (South Indian)",["Non-veg","Celebration","Spicy"],4,"Hard",30,45,"+ 30 min marinating",(720,38,80,26,3),["festive","weekend","party"],"completed",
"""1½–2 cups | basmati rice
500 g | chicken (marinade)
1 tsp | salt (marinade)
1 tsp | red chilli powder (marinade)
⅛ tsp | turmeric (marinade)
½ tsp | pepper powder (marinade)
1 tsp | coriander powder (marinade)
½ tbsp | ginger garlic paste (marinade)
1 tbsp | curd (marinade)
1 tbsp | lemon juice (marinade)
2 tbsp | corn flour (marinade)
2 tbsp | all-purpose flour (marinade)
1 | egg (marinade)
pinch | red food colour (marinade, optional)
1 tsp | ginger garlic paste (biryani masala)
1 tsp | salt (biryani masala)
1 tsp | red chilli powder (biryani masala)
½ tsp | pepper powder (biryani masala)
1 tsp | coriander powder (biryani masala)
1 tsp | biryani masala
some | coriander leaves
some | mint leaves
oil/ghee | for frying and layering""",
["Marinate the chicken with all the marination ingredients for 30 minutes (★ steps written from the ingredient list).",
 "Deep-fry the chicken until crisp — this is your Chicken 65.",
 "Parboil the soaked rice in salted water until 70% cooked; drain.",
 "In 2 tbsp oil/ghee, cook the biryani-masala ingredients with a splash of water for 2 minutes; toss the fried chicken in it.",
 "Layer rice over the chicken with mint and coriander, drizzle ghee, cover and cook on low (dum) for 15–20 minutes.",
 "Fluff gently and serve with raita."],
"Repo caption listed ingredients only; steps written (★).","")
r("chicken-65-garlic-bread","Chicken 65 Garlic Bread","Snack","Indian-Italian fusion",["Non-veg","Party food","Spicy"],4,"Hard",30,60,"+ 2 h marinating",(620,34,48,32,3),["party","movie","weekend"],"completed",
"""500 g | boneless chicken, small cubes
1 tsp | red chilli powder
½ tsp | turmeric
½ tsp | black pepper
1 tbsp | ginger garlic paste
½ tsp | garam masala
to taste | salt
1 tsp | lemon juice
pinch | red food colour (optional)
2 tbsp | cornflour
1 tbsp | all-purpose flour
1 | egg white
¼ tsp | baking soda
as needed | oil, for shallow frying
½ tsp | cumin seeds (sauce)
2 tbsp | chopped garlic (sauce)
2 tbsp | chopped ginger (sauce)
2–3 | green chillies, slit (sauce)
few | curry leaves (sauce)
½ tsp each | black pepper & red chilli powder (sauce)
2 tbsp | red chilli sauce (sauce)
1 | garlic head, for roasting (★ from steps)
60 g | butter (★ from steps)
1 tsp each | oregano, parsley, chilli flakes (★ from steps)
1 | baguette / garlic-bread loaf, halved (★ from steps)
150 g | mozzarella, grated (★ from steps)
to finish | fried curry leaves, red onion, lime (★ from steps)""",
None,"From the repo (caption). Garlic-butter, bread and cheese ingredients appear only in the steps, so they were added (★) with estimated amounts.","")
r("chicken-chukka","Chettinad Chicken Chukka","Main Course","Indian (Chettinad)",["Non-veg","Spicy","Gluten-free"],4,"Medium",20,35,"",(400,34,10,24,3),["rainy","weekend"],"rewritten",
"""750 g | bone-in chicken
3 tbsp | gingelly (sesame) oil
2 | onions, finely chopped
15 | shallots, sliced (optional)
1 tbsp | ginger-garlic paste
1 | tomato, chopped
½ tsp | turmeric
2 sprigs | curry leaves
roast & grind | 6 dried red chillies, 1 tbsp coriander seeds, 1 tsp cumin, 1 tsp fennel, 1½ tsp black peppercorns, 2 cloves, 1 inch cinnamon, 1 tbsp grated coconut""",
["Dry-roast the whole spices and coconut until fragrant; grind to a coarse powder.",
 "Heat oil, add curry leaves, onions and shallots; fry until deep golden.",
 "Add ginger-garlic paste, then tomato and turmeric; cook until soft.",
 "Add chicken and salt; cook covered 15 minutes, stirring now and then.",
 "Add the ground masala and roast uncovered on medium heat until the chicken is dry, dark and coated, 10–15 minutes.",
 "Serve with rice and rasam or parottas."],
"Repo entry pointed at an unrelated French chicken recipe; rewritten as Chettinad chicken chukka.","")
r("chicken-sandwich","Grilled Chicken Club Sandwich","Main Course","American",["Non-veg","High-protein"],2,"Easy",15,15,"",(620,42,46,28,4),["brunch","weeknight"],"rewritten",
"""2 | chicken breasts (about 300 g), butterflied
1 tsp | paprika
½ tsp | garlic powder
1 tbsp | olive oil
6 | slices bread, toasted
4 | strips bacon or chicken/turkey rashers (optional)
3 tbsp | mayonnaise
1 tsp | mustard
4 | lettuce leaves
1 | tomato, sliced
2 | cheese slices""",
["Season chicken with paprika, garlic powder, salt and pepper; grill in olive oil 5–6 minutes per side until cooked through. Rest and slice.",
 "Crisp the bacon (if using).",
 "Spread toast with mayo-mustard. Layer: toast, chicken, cheese, toast, bacon, lettuce, tomato, toast.",
 "Secure with skewers, cut into triangles and serve with chips."],
"Repo entry pointed at an unrelated French chicken recipe; rewritten as a chicken club sandwich.","")
r("chicken-tikka-rice","Chicken Tikka Masala with Jeera Rice","Main Course","British-Indian",["Non-veg","Creamy","Gluten-free"],4,"Medium",25,40,"+ 1 h marinating",(720,40,72,28,4),["rainy","weekend","party"],"rewritten",
"""600 g | boneless chicken thighs
150 g | yogurt
1 tbsp | ginger-garlic paste
2 tsp | garam masala (divided)
1½ tsp | Kashmiri chilli powder
1 tsp | ground cumin
2 tbsp | butter or oil
1 | onion, finely chopped
400 g | crushed tomatoes
120 ml | cream
1 tsp | kasuri methi
1½ cups | basmati rice
1 tsp | cumin seeds
1 tbsp | ghee""",
["Marinate chicken with yogurt, ginger-garlic paste, 1 tsp garam masala, chilli and cumin for 1 hour; grill or broil until charred.",
 "Sauté onion in butter until golden; add tomatoes and simmer 15 minutes.",
 "Stir in cream, kasuri methi and remaining garam masala; add the tikka and simmer 5–8 minutes.",
 "For jeera rice: crackle cumin in ghee, add rinsed rice and 2¾ cups water with salt; cover and cook 12 minutes on low, rest 5.",
 "Serve the masala over the rice."],
"Repo entry reused a fried rice recipe; rewritten as tikka masala with rice.","Often credited to Glasgow’s Shish Mahal restaurant (1970s) and long called a British national dish.")
r("chipotle-chicken-wrap","Chipotle Chicken Wrap","Main Course","Mexican-inspired",["Non-veg","High-protein"],4,"Easy",20,15,"+ 30 min marinating (optional)",(560,40,42,24,4),["weeknight","mealprep","gym"],"completed",
"""500 g | chicken breast or thighs
2–3 | chipotle peppers in adobo
3 | garlic cloves
1 tbsp | lemon juice (marinade)
to taste | salt & pepper
1 tbsp | oil
½ cup | Greek yogurt (sauce)
2 tbsp | mayonnaise (sauce)
1 tsp | lemon juice (sauce)
¼ tsp | garlic powder (sauce)
1 tbsp | chopped parsley
1 cup | mozzarella, shredded
½ | red onion, sliced
1 | bell pepper, sliced
4 | romaine lettuce leaves
4 | large flour tortillas""",
None,"From the repo (caption) — it had steps but no ingredient list, so ingredients were listed from the steps with estimated amounts.","")
r("chipotle-style-burrito-bowl","Chipotle-Style Burrito Bowl","Main Course","Mexican-American",["Non-veg","Meal prep","Gluten-free","High-protein"],4,"Medium",25,30,"",(680,42,78,22,13),["mealprep","weeknight","gym"],"rewritten",
"""600 g | chicken thighs
2 | chipotles in adobo + 1 tbsp adobo
1 tsp each | cumin, oregano, garlic powder
2 tbsp | oil
1½ cups | long-grain rice
1 | lime (zest & juice)
3 tbsp | chopped cilantro
1 can (400 g) | black beans, warmed
1 cup | corn salsa or sweet corn
1 cup | pico de gallo / tomato salsa
1 | avocado or guacamole
½ cup | sour cream or yogurt
1 cup | shredded lettuce
½ cup | cheese""",
["Blend chipotles, adobo, spices, 1 tbsp oil and salt; marinate the chicken (15 minutes minimum).",
 "Cook rice; fold in lime zest, juice, cilantro and salt for cilantro-lime rice.",
 "Grill or pan-sear the chicken 5–6 minutes per side; rest and dice.",
 "Warm the beans with a pinch of cumin and salt.",
 "Build bowls: rice, beans, chicken, corn, salsa, lettuce, cheese, avocado and sour cream."],
"Repo entry had no ingredients or steps; recipe written to match the name.","")
r("chipotle-s-chicken-al-pastor","Chicken Al Pastor (Chipotle-Style)","Main Course","Mexican",["Non-veg","Spicy","Gluten-free"],4,"Medium",20,20,"+ 1 h marinating",(380,36,14,20,2),["party","weekend","mealprep"],"rewritten",
"""700 g | boneless chicken thighs
3 | dried guajillo chillies, soaked (or 2 tbsp ancho/guajillo powder)
1–2 | chipotles in adobo
3 | garlic cloves
½ cup | pineapple chunks (+ more grilled, to serve)
2 tbsp | achiote paste (or 1 tbsp paprika)
2 tbsp | orange juice
1 tbsp | white vinegar
1 tsp | cumin
1 tsp | oregano
1 tbsp | oil
½ | onion, cilantro & lime to serve""",
["Blend chillies, chipotle, garlic, pineapple, achiote, orange juice, vinegar, spices and salt into a smooth marinade.",
 "Coat the chicken and marinate at least 1 hour.",
 "Sear in a hot pan or grill 5–6 minutes per side until charred and cooked through.",
 "Rest, chop finely, and toss with any pan juices.",
 "Serve in tacos or bowls with grilled pineapple, onion, cilantro and lime."],
"Repo entry had no ingredients or steps; recipe written to match the name.","Al pastor descends from shawarma brought to Puebla by Lebanese immigrants.")
r("choco-lava-cake","Healthier Choco Lava Cake","Dessert","International",["Vegetarian","Baking"],4,"Medium",15,17,"+ 2 h freezing ganache",(280,7,34,13,4),["sweet","movie","festive"],"completed",
"""60 g | wholewheat flour or oat flour
20 g | cocoa powder
½ tsp | baking powder
2–3 tbsp | honey (or date paste / maple syrup / jaggery / zero-calorie sweetener)
120 g | milk, room temperature
40 g | dark chocolate, chopped (ganache)
2 tbsp | milk or hot water (ganache)""",
["Ganache: melt the chocolate with milk/hot water over a double boiler; freeze 2 hours or until set, then scoop into 4 balls.",
 "Whisk flour, cocoa and baking powder; stir in the sweetener and milk to a thick batter (★ written).",
 "Half-fill greased ramekins, press a ganache ball into each, cover with the remaining batter (★).",
 "Bake in a preheated oven at 170–180°C for 15–17 minutes (top firm yet jiggly), or air-fry at 150°C for 15–17 minutes.",
 "Rest 2 minutes, invert and serve warm."],
"Repo caption had gram amounts stripped out; amounts estimated, mixing steps written (★). Baking times are from the caption.","Molten cake is usually credited to French chefs and to Jean-Georges Vongerichten in New York (1987).")
r("dragon-chicken","Dragon Chicken","Entree","Indo-Chinese",["Non-veg","Spicy"],3,"Medium",15,20,"",(450,32,26,24,2),["movie","latenight","party"],"rewritten",
"""400 g | boneless chicken, thin strips
1 | egg
3 tbsp | cornflour
1 tbsp | soy sauce (marinade)
1 tsp | ginger-garlic paste
oil | for frying
1 tbsp | chopped garlic
6 | dried red chillies (or 1 tsp chilli flakes)
10 | cashews
1 | onion, sliced
½ | red & green capsicum, strips
2 tbsp | Schezwan or red chilli sauce
1 tbsp | ketchup
1 tsp | honey
1 tsp | vinegar
2 | spring onions""",
["Coat chicken strips with egg, cornflour, soy sauce, ginger-garlic paste and salt. Fry until crisp.",
 "In a hot wok, fry cashews till golden, then garlic and dried chillies for 20 seconds.",
 "Add onion and capsicum strips; toss 1 minute on high heat.",
 "Add Schezwan sauce, ketchup, honey and vinegar; toss in the chicken until glossy and coated.",
 "Finish with spring onions."],
"Repo entry pointed at an unrelated French chicken recipe; rewritten as Indo-Chinese dragon chicken.","")
