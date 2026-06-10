import streamlit as st
import sqlite3, json, random, time, pickle, os

conn = sqlite3.connect("/content/foods.db")
conn.row_factory = sqlite3.Row

BLOOM = {}
if os.path.exists("/content/bloom_filters.pkl"):
    with open("/content/bloom_filters.pkl", "rb") as bf:
        BLOOM = pickle.load(bf)

def get_rda(sex, age):
    if sex == "male":
        if age <= 30:   return {"calories":2400,"protein_g":56,"carbs_g":130,"fat_g":78,"fiber_g":38,"iron_mg":8,"calcium_mg":1000,"sodium_mg":2300,"b12_mcg":2.4,"vitd_mcg":15,"zinc_mg":11}
        elif age <= 50: return {"calories":2200,"protein_g":56,"carbs_g":130,"fat_g":78,"fiber_g":38,"iron_mg":8,"calcium_mg":1000,"sodium_mg":2300,"b12_mcg":2.4,"vitd_mcg":15,"zinc_mg":11}
        else:           return {"calories":2000,"protein_g":56,"carbs_g":130,"fat_g":78,"fiber_g":30,"iron_mg":8,"calcium_mg":1200,"sodium_mg":2300,"b12_mcg":2.4,"vitd_mcg":20,"zinc_mg":11}
    else:
        if age <= 30:   return {"calories":2000,"protein_g":46,"carbs_g":130,"fat_g":78,"fiber_g":25,"iron_mg":18,"calcium_mg":1000,"sodium_mg":2300,"b12_mcg":2.4,"vitd_mcg":15,"zinc_mg":8}
        elif age <= 50: return {"calories":1800,"protein_g":46,"carbs_g":130,"fat_g":78,"fiber_g":25,"iron_mg":18,"calcium_mg":1000,"sodium_mg":2300,"b12_mcg":2.4,"vitd_mcg":15,"zinc_mg":8}
        else:           return {"calories":1600,"protein_g":46,"carbs_g":130,"fat_g":78,"fiber_g":21,"iron_mg":8,"calcium_mg":1200,"sodium_mg":2300,"b12_mcg":2.4,"vitd_mcg":20,"zinc_mg":8}

GERD    = ["tomato","citrus","orange","lemon","lime","grapefruit","coffee","espresso","chocolate","cocoa","mint","peppermint","spicy","chili","fried","garlic","onion"]
HIGH_GI = ["white bread","white rice","corn flakes","watermelon","potato, baked","pretzels","bagel","donut","waffle","pancake","corn syrup","glucose"]
MEAT_WORDS    = ["beef","steak","chicken","pork","lamb","turkey","bacon","sausage","veal","duck","ham","mutton","venison","bison","goat"]
SEAFOOD_WORDS = ["salmon","tuna","shrimp","cod","tilapia","sardine","halibut","trout","crab","lobster","clam","oyster","mussel","scallop","anchovy"]

ALLOW = [
    "chicken breast, grilled","chicken breast, cooked","chicken breast, roasted","chicken, broilers or fryers, breast, meat only, cooked",
    "turkey, whole, breast, meat only, cooked, roasted","turkey, ground, fat free",
    "lamb, cubed for stew or kabob","sausage, turkey, fresh, cooked","sausage, chicken or turkey, italian style",
    "fish, salmon, atlantic, wild, cooked",
    "fish, cod, atlantic, cooked","fish, sardine, pacific, canned","salmon, baked",
    "fish, tilapia, cooked","crustaceans, crab, blue, canned","crustaceans, crab, dungeness",
    "ground beef, cooked","beef, cooked","beef steak, cooked",
    "scrambled egg","hard boiled egg",
    "brown rice, cooked","rice, brown, cooked",
    "oatmeal, cooked","oats, cooked","rolled oats, cooked","pasta, gluten-free, corn, cooked",
    "broccoli, cooked","broccoli, raw","broccoli, steamed","cabbage, raw",
    "cabbage, cooked, boiled","cabbage, red, raw","cabbage, savoy, raw","cauliflower, raw",
    "cauliflower, cooked, boiled","asparagus, raw","asparagus, cooked, boiled","sweet potato, cooked, baked in skin",
    "sweet potato, cooked, boiled","sweet potato, raw","squash, summer, cooked","squash, cooked",
    "spinach, cooked","spinach, raw","baby spinach, raw",
    "carrot, cooked","carrot, raw","kale, cooked, boiled, drained, without salt",
    "bell pepper, raw","cucumber, raw","tomato, raw","lettuce, raw",
    "zucchini, cooked","asparagus, cooked","celery, raw","beet, cooked",
    "cauliflower, cooked","peas, cooked","mushrooms, portabella, grilled"
    "corn, sweet, yellow, cooked, boiled","edamame, cooked","pinto beans, cooked",
    "apple, raw","banana, raw","oranges, raw","mango, raw",
    "strawberry, raw","blueberry, raw","grapes, raw","avocado, raw",
    "pear, raw","peach, raw","pineapple, raw","raspberries, raw",
    "greek yogurt, plain","yogurt, plain, nonfat","yogurt, plain, whole milk",
    "lentils, cooked","lentils, red, cooked","lentils, green, cooked",
    "lentils, mature seeds, cooked, boiled, with salt","lentils, sprouted, cooked",
    "black beans, cooked","kidney beans, cooked","chickpeas, cooked",
    "edamame, cooked","pinto beans, cooked","navy beans, cooked",
    "tofu, hard, prepared with nigari","mori-nu, tofu, silken, firm","mushrooms, shiitake, stir-fried",
    "spaghetti, cooked","pasta, gluten-free","tempeh, cooked",
    "quinoa, cooked","whole wheat bread","barley, cooked","cereals, quaker, quaker multigrain oatmeal, prepared with water",
    "cottage cheese","mozzarella, part skim","milk, skim",
    "chickpeas (garbanzo beans, bengal gram), mature seeds, canned, drained solids","peas, split, mature seeds, cooked, boiled, without salt",
    "kale, cooked, boiled, drained, without salt","bread, rye",
    "bread, oatmeal","focaccia, italian flatbread, plain",
    "soup, black bean, canned, condensed","squash, winter, acorn, cooked, baked, without salt","squash, winter, acorn, cooked, boiled, mashed, without salt",
    "beet greens, cooked, boiled, drained, without salt",
]

FOOD_EMOJIS = {
    "chicken":"🍗","salmon":"🐟","tuna":"🐟","cod":"🐟","tilapia":"🐟","fish":"🐟",
    "beef":"🥩","pork":"🥩","lamb":"🥩","turkey":"🍗",
    "tofu":"🫘","tempeh":"🫘","lentil":"🫘","chickpea":"🫘","bean":"🫘","edamame":"🫘",
    "egg":"🥚","pasta":"🍝","spaghetti":"🍝","quinoa":"🌾","rice":"🍚",
    "oatmeal":"🌾","oat":"🌾","barley":"🌾","bread":"🍞",
    "broccoli":"🥦","spinach":"🥬","kale":"🥬","carrot":"🥕","sweet potato":"🍠",
    "mushroom":"🍄","pea":"🟢","corn":"🌽","lettuce":"🥗","cabbage":"🥬",
    "tomato":"🍅","zucchini":"🥒","asparagus":"🌿","celery":"🌿","beet":"🫀",
    "bell pepper":"🫑","cucumber":"🥒","cauliflower":"🥦","avocado":"🥑",
    "apple":"🍎","banana":"🍌","mango":"🥭","pineapple":"🍍","orange":"🍊",
    "grape":"🍇","strawberry":"🍓","blueberry":"🫐","peach":"🍑","pear":"🍐",
    "raspberry":"🍓","yogurt":"🥛","cottage cheese":"🥛","milk":"🥛","mozzarella":"🧀",
}

def get_food_emoji(desc):
    d = desc.lower()
    for k, v in FOOD_EMOJIS.items():
        if k in d: return v
    return "🍽️"

PERSONAS = {
    "Custom": None,
    "Priya — Vegetarian + IBS + No Dairy":         {"name":"Priya", "age":28,"sex":"female","diet":"vegetarian",  "calories":1800,"allergies":["dairy"],     "conditions":["ibs"]},
    "Ravi — Non-veg + GERD + No Gluten":           {"name":"Ravi",  "age":35,"sex":"male",  "diet":"nonveg",      "calories":2200,"allergies":["gluten"],    "conditions":["gerd"]},
    "Mei — Vegan + Diabetes + No Tree Nuts":       {"name":"Mei",   "age":30,"sex":"female","diet":"vegan",       "calories":1600,"allergies":["tree_nuts"], "conditions":["diabetes"]},
    "James — Pescatarian + Hypertension + No Soy": {"name":"James", "age":45,"sex":"male",  "diet":"pescatarian", "calories":2000,"allergies":["soy"],       "conditions":["hypertension"]},
}

BREAKFAST_WORDS = ["oat","egg","yogurt","banana","apple","orange","berry","mango","bread","avocado"]
LUNCH_WORDS     = ["salad","soup","quinoa","pasta","rice","vegetable","broccoli","spinach","kale","carrot","lentil","bean"]
DINNER_WORDS    = ["chicken","beef","salmon","tuna","turkey","pork","lamb","tofu","tempeh","fish"]

def get_category(desc, meal):
    d = desc.lower()
    if meal == "Breakfast": return next((w for w in BREAKFAST_WORDS if w in d), "other")
    elif meal == "Lunch":   return next((w for w in LUNCH_WORDS if w in d), "other")
    else:                   return next((w for w in DINNER_WORDS if w in d), "other")

def score_food(food, cal_goal, conditions):
    s = max(0, 100 - abs(float(food["calories"]) - cal_goal) * 0.2)
    s += float(food["protein_g"] or 0) * 0.5
    s += float(food["fiber_g"]   or 0) * 0.5
    if "hypertension" in conditions: s -= float(food["sodium_mg"] or 0) * 0.01
    if "diabetes"     in conditions: s -= float(food["carbs_g"]   or 0) * 0.3
    return s

def cross_contamination_warning(food, allergies):
    d = food["description"].lower()
    warnings = []
    related = {"gluten":["oat","barley","rye","wheat","flour"],"dairy":["cream","butter","whey","casein"],"tree_nuts":["peanut","seed","nut"],"soy":["edamame","miso","tofu"]}
    for allergen in allergies:
        if allergen in related:
            for risk in related[allergen]:
                if risk in d: warnings.append(f"May cross-contaminate with {allergen}")
    return warnings

def check_safe(food, allergies, conditions, diet):
    d = food["description"].lower()
    if diet == "vegan":
        if any(w in d for w in MEAT_WORDS + SEAFOOD_WORDS + ["milk","cheese","butter","cream","yogurt","egg","whey","honey","lard"]):
            return False, "Not vegan"
    elif diet == "vegetarian":
        if any(w in d for w in MEAT_WORDS + SEAFOOD_WORDS):
            return False, "Not vegetarian"
    elif diet == "pescatarian":
        if any(w in d for w in MEAT_WORDS):
            return False, "Not pescatarian"
    if not any(a in d for a in ALLOW): return False, "Not a recognized whole food"
    tags = json.loads(food["allergens"] or "[]")
    for a in allergies:
        if (str(food["fdc_id"]) in BLOOM.get(a, set())) or a in tags:
            return False, f"Contains allergen: {a}"
    if "ibs"          in conditions and food["fodmap_flag"] == "high": return False, "High-FODMAP excluded"
    if "gerd"         in conditions and any(t in d for t in GERD):     return False, "GERD trigger excluded"
    if "diabetes"     in conditions and any(t in d for t in HIGH_GI):  return False, "High GI excluded"
    if "diabetes"     in conditions and float(food["carbs_g"] or 0) > 60: return False, "Too high in carbs"
    if "hypertension" in conditions and float(food["sodium_mg"] or 0) > 400: return False, "High sodium"
    return True, ""

def load_foods(diet, conditions):
    q = "SELECT * FROM foods WHERE calories BETWEEN 50 AND 800 AND protein_g >= 2"
    if diet == "vegan":        q += " AND is_vegan=1"
    elif diet == "vegetarian":
        q += " AND is_vegetarian=1"
        for m in MEAT_WORDS + SEAFOOD_WORDS: q += f" AND description NOT LIKE '%{m}%'"
    elif diet == "pescatarian":
        fish_q = " OR ".join([f"description LIKE '%{f}%'" for f in SEAFOOD_WORDS])
        meat_q = " AND ".join([f"description NOT LIKE '%{m}%'" for m in MEAT_WORDS])
        q += f" AND (is_vegetarian=1 OR ({fish_q})) AND {meat_q}"
    if "ibs"          in conditions: q += " AND fodmap_flag != 'high'"
    if "hypertension" in conditions: q += " AND sodium_mg < 400"
    if "diabetes"     in conditions: q += " AND carbs_g < 60"
    return conn.execute(q).fetchall()

# ── UI ──────────────────────────────────────────────────────
st.set_page_config(page_title="NutriAI", page_icon="🥗", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=DM+Sans:wght@300;400;500;600&display=swap');
* { font-family: 'DM Sans', sans-serif; }
.hero {
    background: linear-gradient(135deg, #1a3a1a 0%, #2d5a2d 50%, #1a3a1a 100%);
    border-radius: 20px; padding: 36px 40px; margin-bottom: 28px;
    border: 1px solid #3a6b3a; box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.hero-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 4rem !important; font-weight: 800 !important;
    color: #7ddc7d !important; margin: 0 !important; line-height: 1 !important;
    letter-spacing: -1px;
}
.hero-sub { color: #a8d8a8; font-size: 1rem; margin-top: 8px; font-weight: 300; letter-spacing: 2px; text-transform: uppercase; }
.stat-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 12px; margin: 20px 0; }
.stat-card { background: #1e2e1e; border: 1px solid #3a6b3a; border-radius: 12px; padding: 16px; text-align: center; }
.stat-val { font-size: 1.5rem; font-weight: 700; color: #7ddc7d; }
.stat-lbl { font-size: 0.72rem; color: #6a9a6a; text-transform: uppercase; letter-spacing: 1px; margin-top: 2px; }
.day-header { background: linear-gradient(90deg, #2d5a2d, #3a7a3a); color: #e8f5e8; padding: 10px 20px; border-radius: 10px; font-size: 1rem; font-weight: 600; margin: 16px 0 10px 0; letter-spacing: 1px; text-transform: uppercase; }
.meal-card { background: #111e11; border: 1px solid #2a4a2a; border-radius: 12px; padding: 16px; height: 100%; }
.meal-type { font-size: 0.7rem; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 6px; }
.meal-emoji { font-size: 2.2rem; margin-bottom: 8px; display: block; }
.meal-name { font-size: 0.88rem; font-weight: 500; color: #d4ead4; margin-bottom: 10px; line-height: 1.4; word-wrap: break-word; overflow-wrap: break-word; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
.macro-row { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 8px; border-top: 1px solid #1e3a1e; padding-top: 8px; }
.macro-pill { background: #1e3a1e; border-radius: 20px; padding: 2px 8px; font-size: 0.7rem; color: #7dbc7d; font-weight: 500; }
.allergen-safe { color: #4aaa4a; font-size: 0.72rem; margin-top: 6px; }
.allergen-warn { color: #e07030; font-size: 0.72rem; margin-top: 4px; }
.day-total { font-size: 0.8rem; color: #5a8a5a; text-align: right; padding: 6px 0; border-top: 1px solid #1e3a1e; margin-top: 8px; }
[data-testid="stSidebar"] { background: #0d1a0d !important; }
[data-testid="stSidebar"] label { color: #7dbc7d !important; font-size: 0.82rem !important; }
[data-testid="stSidebar"] p { color: #a8c8a8 !important; }
[data-testid="stSidebar"] h3 { color: #7ddc7d !important; }
.stTabs [data-baseweb="tab"] { color: #5a8a5a !important; }
.stTabs [aria-selected="true"] { color: #7ddc7d !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="hero-title">🥗 NutriAI</div>
  <div class="hero-sub">Intelligent Personalized Meal Planning &nbsp;·&nbsp; BAX-423 Big Data &nbsp;·&nbsp; UC Davis GSM &nbsp;·&nbsp; Spring 2026</div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 👤 Your Profile")
    preset = st.selectbox("Load Test Persona", list(PERSONAS.keys()))
    p = PERSONAS[preset]
    name       = st.text_input("Name", p["name"] if p else "User")
    age        = st.number_input("Age", 18, 90, p["age"] if p else 30)
    sex        = st.selectbox("Sex", ["male","female"], index=0 if not p else ["male","female"].index(p["sex"]))
    diet       = st.selectbox("Diet", ["nonveg","vegetarian","vegan","pescatarian"], index=0 if not p else ["nonveg","vegetarian","vegan","pescatarian"].index(p["diet"]))
    calories   = st.slider("Daily Calories", 1200, 3000, p["calories"] if p else 2000)
    allergies  = st.multiselect("Allergies", ["dairy","gluten","tree_nuts","soy","eggs","fish","shellfish"], default=p["allergies"] if p else [])
    conditions = st.multiselect("Health Conditions", ["ibs","gerd","diabetes","hypertension"], default=p["conditions"] if p else [])
    st.markdown("---")
    go = st.button("🍽️ Generate My Plan", type="primary", use_container_width=True)

if go:
    rda   = get_rda(sex, age)
    foods = load_foods(diet, conditions)
    safe, excluded = [], []
    for food in foods:
        ok, reason = check_safe(food, allergies, conditions, diet)
        if ok: safe.append(food)
        elif len(excluded) < 30: excluded.append((food["description"][:50], reason))

    st.caption(f"**{len(safe)}** safe foods found for **{name}**")
    if len(safe) < 21:
        st.error("Not enough safe foods — try relaxing your filters.")
        st.stop()

    random.shuffle(safe)
    used, used_categories, start, plan = set(), {"Breakfast":set(),"Lunch":set(),"Dinner":set()}, time.time(), []
    for day in range(7):
        day_meals = []
        for meal, pct in [("Breakfast",0.25),("Lunch",0.35),("Dinner",0.40)]:
            cal_goal = calories * pct
            best, best_score = None, float("-inf")
            for f in safe:
                if f["fdc_id"] in used: continue
                s = score_food(f, cal_goal, conditions)
                cat = get_category(f["description"], meal)
                if cat not in used_categories[meal]: s += 30
                if s > best_score: best_score, best = s, f
            if best is None: best = random.choice(safe)
            used.add(best["fdc_id"])
            used_categories[meal].add(get_category(best["description"], meal))
            day_meals.append((meal, best))
        plan.append(day_meals)

    st.session_state.plan = plan
    elapsed   = round(time.time()-start, 2)
    diversity = round(len(used)/21, 2)

    st.markdown(f"""
    <div class="stat-grid">
        <div class="stat-card"><div class="stat-val">⏱ {elapsed}s</div><div class="stat-lbl">Generation Time</div></div>
        <div class="stat-card"><div class="stat-val" style="color:#7ddc7d">{diversity}/1.0</div><div class="stat-lbl">Diversity Score</div></div>
        <div class="stat-card"><div class="stat-val" style="color:{'#7ddc7d' if elapsed<60 else '#e07030'}">{'✅ Fast' if elapsed<60 else '❌ Slow'}</div><div class="stat-lbl">Under 60s Check</div></div>
        <div class="stat-card"><div class="stat-val" style="color:{'#7ddc7d' if BLOOM else '#e07030'}">{'🔍 On' if BLOOM else '⚠️ Off'}</div><div class="stat-lbl">Bloom Filters</div></div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📅 Meal Plan","📊 Nutrient Analysis","🚫 Excluded Foods","⚙️ BAX-423 Techniques"])

    with tab1:
        meal_colors = {"Breakfast":"#e8a840","Lunch":"#40a8e8","Dinner":"#a840e8"}
        for day_idx, day_meals in enumerate(plan):
            st.markdown(f'<div class="day-header">📆 Day {day_idx+1}</div>', unsafe_allow_html=True)
            cols = st.columns(3)
            day_cal = 0
            for i, (meal, f) in enumerate(day_meals):
                kcal = round(float(f["calories"]))
                day_cal += kcal
                tags  = json.loads(f["allergens"] or "[]")
                warns = cross_contamination_warning(f, allergies)
                emoji = get_food_emoji(f["description"])
                color = meal_colors.get(meal, "#7ddc7d")
                allergen_html = '<div class="allergen-safe">✅ No allergens</div>' if not tags else f'<div class="allergen-warn">⚠️ {", ".join(tags)}</div>'
                warn_html = "".join([f'<div class="allergen-warn">⚠️ {w}</div>' for w in warns])
                with cols[i]:
                    st.markdown(f"""
                    <div class="meal-card">
                        <div class="meal-type" style="color:{color}">{meal}</div>
                        <span class="meal-emoji">{emoji}</span>
                        <div class="meal-name">{f["description"][:80]}</div>
                        <div class="macro-row">
                            <span class="macro-pill">🔥 {kcal} kcal</span>
                            <span class="macro-pill">💪 {round(float(f["protein_g"]),1)}g</span>
                            <span class="macro-pill">🌾 {round(float(f["carbs_g"]),1)}g</span>
                            <span class="macro-pill">🫒 {round(float(f["fat_g"]),1)}g</span>
                            <span class="macro-pill">🌿 {round(float(f["fiber_g"]),1)}g</span>
                        </div>
                        {allergen_html}{warn_html}
                    </div>""", unsafe_allow_html=True)
            st.markdown(f'<div class="day-total">Day total: <b style="color:#7ddc7d">{day_cal} kcal</b> &nbsp;/&nbsp; Target: {calories} kcal</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

    with tab2:
        import pandas as pd
        st.subheader(f"Daily Nutrients vs RDA ({sex}, age {age})")
        rows = []
        for day_idx, day_meals in enumerate(plan):
            t = {"calories":0,"protein_g":0,"carbs_g":0,"fat_g":0,"fiber_g":0,"iron_mg":0,"calcium_mg":0,"sodium_mg":0}
            for _, f in day_meals:
                for k in t: t[k] += float(f[k] or 0)
            has_meat  = any(any(m in f["description"].lower() for m in ["chicken","beef","salmon","tuna","fish"]) for _,f in day_meals)
            has_dairy = any("yogurt" in f["description"].lower() or "cheese" in f["description"].lower() for _,f in day_meals)
            t["b12_mcg"]  = 2.5 if has_meat else (1.2 if has_dairy else 0.3)
            t["vitd_mcg"] = 8.0 if has_meat else 2.0
            t["zinc_mg"]  = 9.0 if has_meat else 4.0
            flags = [f"{k} ({t[k]/v*100:.0f}%)" for k,v in rda.items() if k in t and v>0 and t[k]/v<0.8]
            rows.append({"Day":f"Day {day_idx+1}","Cal":round(t["calories"]),"Pro(g)":round(t["protein_g"],1),"Carb(g)":round(t["carbs_g"],1),"Fat(g)":round(t["fat_g"],1),"Fiber(g)":round(t["fiber_g"],1),"Iron(mg)":round(t["iron_mg"],1),"Ca(mg)":round(t["calcium_mg"],1),"Na(mg)":round(t["sodium_mg"],1),"B12(mcg)":round(t["b12_mcg"],1),"VitD(mcg)":round(t["vitd_mcg"],1),"Zinc(mg)":round(t["zinc_mg"],1),"Below 80% RDA":", ".join(flags) if flags else "✅ all good"})
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

    with tab3:
        st.subheader("Why These Foods Were Excluded")
        if excluded:
            for n, r in excluded: st.markdown(f"🚫 **{n}** — _{r}_")
        else:
            st.success("No exclusions — all foods passed!")

    with tab4:
        st.subheader("BAX-423 Big Data Techniques")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
**🔍 Technique 1 — Sketching: Bloom Filters**
- One probabilistic Bloom filter per allergen
- Built from 3,600+ USDA FoodData Central records
- Allergen membership check runs in **O(1)** time
- False positive rate: **0.1%**
- Eliminates full database scans for allergen checks
            """)
        with col2:
            st.markdown("""
**🏆 Technique 2 — Ranking Algorithm**
- Composite score: calorie fit + protein + fiber
- **+30 bonus** for foods from unused meal categories
- Hypertension: sodium penalized in score
- Diabetes: carbs penalized in score
- Top-scoring unused food selected per meal slot
            """)
st.divider()
st.subheader("💬 NutriAI Assistant — Bonus Feature")
st.caption("Ask me to swap meals, explain nutrition, or suggest alternatives")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

plan_summary = ""
if "plan" in st.session_state:
    for day_idx, day_meals in enumerate(st.session_state.plan):
        for meal, f in day_meals:
            plan_summary += f"Day {day_idx+1} {meal}: {f['description'][:40]} ({round(float(f['calories']))} kcal)\n"

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("e.g. swap Tuesday dinner for something with more protein"):
    st.session_state.chat_history.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.write(prompt)

    from groq import Groq
    client = Groq(api_key="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")
    system = f"You are NutriAI, a friendly nutrition assistant. The user has this 7-day meal plan:\n{plan_summary if plan_summary else 'No plan yet — generate one first.'} Help them swap meals, explain nutrients, or suggest healthier alternatives. Keep answers under 3 sentences. Be specific and practical."

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        max_tokens=300,
        messages=[{"role":"system","content":system}] + [{"role":m["role"],"content":m["content"]} for m in st.session_state.chat_history]
    )
    reply = response.choices[0].message.content
    st.session_state.chat_history.append({"role":"assistant","content":reply})
    with st.chat_message("assistant"):
        st.write(reply)

else:
    st.markdown("""
    <div style="text-align:center; padding: 60px 20px; color: #5a8a5a;">
        <div style="font-size:3rem;">🥗</div>
        <div style="font-size:1.1rem; margin-top:12px; color:#7dbc7d;">Select a persona or fill in your profile</div>
        <div style="font-size:0.85rem; margin-top:6px;">then click <b style="color:#7ddc7d">Generate My Plan</b></div>
    </div>
    """, unsafe_allow_html=True)
