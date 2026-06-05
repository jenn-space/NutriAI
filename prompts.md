# Key AI Prompts Used — NutriAI
**BAX-423 Big Data · Jenn Tran · Spring 2026**

AI tool used: Claude (Anthropic). All code was reviewed, tested, and modified by the student.

---

## Prompt 1 — Data Pipeline
**Prompt:** "Give me a Python pipeline that fetches clean real foods from the USDA FoodData Central API using SR Legacy, Foundation, and Survey FNDDS data types, filters by CLEAN_KEYWORDS to only keep whole foods, fetches real nutrient values using the POST /foods endpoint in batches of 20, and saves to SQLite. Target 10,000 records."

**Used for:** data_pipeline.py — building the 10,011-food database.

**Modified:** Added JUNK blocklist to filter processed foods. Added Survey (FNDDS) and Branded data types to reach 10k. Tuned CLEAN_KEYWORDS to use USDA-style phrases like "broccoli, cooked, boiled" instead of just "broccoli".

---

## Prompt 2 — Bloom Filters
**Prompt:** "Build Bloom filters for allergen detection using pybloom-live. One filter per allergen built from all fdc_ids in foods.db. Allergen check O(1) with 0.1% false positive rate."

**Used for:** bloom_builder.py — the allergen detection system.

**Modified:** Increased capacity from 15,000 to 20,000 to accommodate 10k food database.

---

## Prompt 3 — Diet Filtering Fix
**Prompt:** "Fix the vegetarian filter to block meat even when the is_vegetarian DB flag is wrong. Use dual-layer: SQL NOT LIKE for meat words, and Python check_safe() that receives diet as a parameter and checks MEAT_WORDS and SEAFOOD_WORDS against the food description."

**Used for:** Diet filtering logic in app.py.

**Modified:** Added vegan-specific blocking of dairy/eggs/honey. Added pescatarian logic allowing seafood but blocking meat.

---

## Prompt 4 — ALLOW List Debugging
**Prompt:** "My app shows 0 safe foods for vegetarian diet. Check what vegan foods actually exist in the database and give me exact USDA-style phrases to use in the ALLOW list."

**Used for:** Debugging and fixing the ALLOW list in app.py.

**Modified:** Ran DB queries to find exact USDA food names, replaced generic phrases like "broccoli" with USDA-exact names like "broccoli, cooked, boiled, drained, without salt" and specific tofu/tempeh brand names.

---

## Prompt 5 — UI Design
**Prompt:** "Redesign the Streamlit UI with dark forest green theme, Playfair Display serif font for the title, food emoji icons auto-assigned by food type, meal cards with colored macro pills, 4-stat header row, and persona dropdown that auto-fills all fields."

**Used for:** Full UI redesign in write_app.py.

**Modified:** Adjusted color scheme to #1a3a1a for darker feel. Added meal type color coding (gold=breakfast, blue=lunch, purple=dinner). Added -webkit-line-clamp:3 to prevent food names overflowing cards. Added persona presets for all 4 rubric test personas.

---

## Prompt 6 — Chatbot Integration
**Prompt:** "Add a Groq-powered chatbot to the Streamlit app that knows the user's current 7-day meal plan and can answer questions like swap Tuesday dinner for something with more protein. Use llama-3.1-8b-instant model and store the plan in st.session_state."

**Used for:** Bonus chatbot feature in app.py.

**Modified:** Switched from Anthropic API to Groq (free). Updated model from llama3-8b-8192 (decommissioned) to llama-3.1-8b-instant. Added plan context to system prompt so chatbot knows exact meal names and calories.

---

## Prompt 7 — Persona Test
**Prompt:** "Write a persona test cell that runs all 4 rubric personas (Priya, Ravi, Mei, James) against the database and shows safe food count, diversity score, time, and PASS/FAIL for each."

**Used for:** Validating all 4 personas before submission.

**Modified:** Added allergen violation check and diet violation check to catch edge cases where wrong foods slip through.
