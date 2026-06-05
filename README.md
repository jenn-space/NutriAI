# NutriAI
AI-powered diet planner


---

## Live Demo
The app runs via Streamlit + ngrok. To generate a live URL run the Colab notebook (see Setup below).

**Source Code Repository:** https://github.com/jenn-space/NutriAI

---

## What It Does
NutriAI generates a personalized 7-day, 3-meal-a-day dietary plan in under 60 seconds. It filters 10,000+ foods from the USDA FoodData Central database by dietary preference, allergies, and clinical conditions using two BAX-423 techniques: Bloom filters (sketching) and a ranking algorithm. Includes a Groq-powered AI chatbot for meal swaps.

---

## Setup Instructions

### Requirements
- Google Colab (free tier works)
- Python 3.10+
- ngrok account (free) — https://ngrok.com
- Groq API key (free) — https://console.groq.com
- USDA API key (free) — https://fdc.nal.usda.gov/api-guide.html

### Step 1 — Install packages
```bash
!pip install streamlit pyngrok pybloom-live requests pandas groq -q
```

### Step 2 — Mount Google Drive and load files
```python
from google.colab import drive
drive.mount('/content/drive')
import shutil
shutil.copy("/content/drive/MyDrive/nutri_ai/foods.db", "/content/foods.db")
shutil.copy("/content/drive/MyDrive/nutri_ai/bloom_filters.pkl", "/content/bloom_filters.pkl")
```

### Step 3 — Write the app
```python
exec(open("/content/app.py").read())
```

### Step 4 — Launch
```python
import subprocess, time
from pyngrok import ngrok, conf

conf.get_default().auth_token = "YOUR_NGROK_TOKEN"
subprocess.Popen(["streamlit","run","/content/app.py","--server.port=8501","--server.headless=true"],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(6)
print(ngrok.connect(8501))
```

Open the printed URL in your browser.

---

## Run Command
```bash
streamlit run app.py
```

---

## File Structure
```
code/
  app.py               # Main Streamlit app
  requirements.txt     # Python dependencies
  README.md            # This file
  prompts.md           # Key AI prompts used

data/
  foods.db             # SQLite database (10,000+ foods)
  bloom_filters.pkl    # Pre-built Bloom filters

brief.pdf              # 4-page technical brief
prompts.md             # Key AI prompts used
```

---

## How to Set Up GitHub Repository
1. Go to https://github.com/new
2. Name it `NutriAI-BAX423` — set to **Public**
3. Click **Create repository**
4. Upload these files from your `code/` folder:
   - `app.py`
   - `requirements.txt`
   - `README.md`
   - `prompts.md`
5. Copy your repo URL and replace `YOUR_GITHUB` in the Live Demo section above

---

## Test Personas — All PASS
| Persona | Diet | Condition | Allergy | Safe Foods | Time |
|---|---|---|---|---|---|
| Priya | Vegetarian | IBS | Dairy | 1,639 | 0.19s |
| Ravi | Non-veg | GERD | Gluten | 5,602 | 0.22s |
| Mei | Vegan | Diabetes | Tree nuts | 1,140 | 0.03s |
| James | Pescatarian | Hypertension | Soy | 2,329 | 0.06s |

---

## BAX-423 Techniques
1. **Bloom Filters (Sketching)** — O(1) allergen checks, 0.1% false positive rate, capacity 20,000
2. **Ranking Algorithm** — composite score: calorie fit + protein + fiber + category diversity bonus (+30)

---

## Data Sources
- USDA FoodData Central API — https://fdc.nal.usda.gov
- Monash University Low-FODMAP List — https://www.monashfodmap.com
- NIH Dietary Reference Intakes — https://www.ncbi.nlm.nih.gov/books/NBK56068
- DASH Diet Guidelines — https://www.nhlbi.nih.gov/education/dash-eating-plan

---

## Limitations
- Food quality: USDA has raw ingredients not recipes. Production version would use Edamam or Spoonacular recipe API
- Vitamin B12, D, Zinc: estimated from food type since USDA SR Legacy doesn't store them consistently
- Hosted via ngrok: URL is only live when Colab session is running
