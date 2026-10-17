# Poojith's Cookbook

A searchable recipe site built from all 492 dishes in [poojithmalla8/cooking_recipe](https://github.com/poojithmalla8/cooking_recipe) (`data/recipes-*.json`, rebuilt from commit a60499a).

Live: https://mad08011999-cloud.github.io/cooking-recipes/

## Data honesty
Every dish has a badge saying where its recipe comes from:

| Badge | Meaning | Count |
|---|---|---|
| From repo | ingredients and steps used as-is from the repo (lightly cleaned: nutrition lines, duplicate steps and hashtag lines removed) | 150 |
| From repo (earlier version) | the repo's current steps belong to another post, so the matching steps from the repo's own earlier commit are used | 2 |
| Repo + filled in ★ | repo ingredients kept, missing steps filled in (★) | 9 |
| Rewritten | repo entry is still empty or a placeholder (an unrelated TheMealDB recipe), so a standard recipe for the dish is shown | 21 |
| Partial in repo | repo has only some of the ingredients or steps; shown as they are | 99 |
| Check | repo steps don't match its ingredients; both are shown, with a warning | 6 |
| Recipe missing in repo | no usable recipe in the repo; the dish is listed with a YouTube search link | 205 |

Values the repo or post doesn't state (times, servings, difficulty, calories, macros, moods) are estimates and are marked `est.` / `~`. "from post" means the original post gave that number. Dish photos are shown only when the linked TheMealDB meal really is this dish.

## Sign in (Supabase, same project as the movie site)
Google, email + password, magic link and password reset, all through Supabase Auth. Only the public publishable key is in the code; no secrets are committed. Saved and Cooked lists sync to the `recipe_status` table once it exists. Until then they stay in the browser.

One-time setup by the project owner:
1. Run `supabase_recipe_status.sql` in the Supabase SQL editor (creates the table and row-level security policies).
2. Under Supabase → Authentication → URL Configuration → Redirect URLs, add `https://mad08011999-cloud.github.io/cooking-recipes/`.

Rebuild: `python3 scripts/fetch_origins2.py && python3 scripts/build2.py` (expects the repo cloned at /tmp/cr2).
