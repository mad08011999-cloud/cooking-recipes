# Poojith's Cookbook

A searchable recipe site built from the 52 recipes in [poojithmalla8/cooking_recipe](https://github.com/poojithmalla8/cooking_recipe) (`data/recipes-01.json`).

Live: https://mad08011999-cloud.github.io/cooking-recipes/

- Category tabs (Breakfast, Entrée/Starter, Snack, Main Course, Side Dish, Dessert), cuisine, diet, time and calorie filters, tags, "comfy time to cook" moods, search across names and ingredients.
- Each recipe shows ingredients with quantities, numbered steps (tap to tick off), prep/cook/total time, servings, difficulty, nutrition per serving, best times to cook, and a "Where it comes from" panel (place photo from Wikimedia Commons plus Wikipedia gists, with credits).
- **Estimated values**: times, servings, difficulty, calories and macros, and moods are estimates and are marked `est.` in the UI. Figures the original post stated are shown as "post said".
- Data badges: *From repo*, *Repo + filled in ★*, or *Rewritten* (used when the repo entry was empty or pointed at an unrelated placeholder recipe). The original repo values are listed in every recipe.

Rebuild: `python3 scripts/fetch_origins.py && python3 scripts/build.py path/to/recipes-01.json`
