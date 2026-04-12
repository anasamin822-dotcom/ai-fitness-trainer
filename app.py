import streamlit as st
import time
import random

st.set_page_config(page_title="AI Fitness Trainer", layout="wide")

# =========================
# 🎨 UI
# =========================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

h1 {
    text-align: center;
    font-size: 55px;
    font-weight: bold;
    background: linear-gradient(90deg, #00f5a0, #00d9f5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

div[data-baseweb="input"], div[data-baseweb="select"] {
    background: rgba(255,255,255,0.08);
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.15);
}

.card {
    background: rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 16px;
    margin: 15px 0;
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255,255,255,0.15);
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-8px);
    box-shadow: 0 0 25px rgba(0,255,170,0.5);
}

.card-title {
    font-size: 22px;
    color: #00f5a0;
    margin-bottom: 10px;
    font-weight: bold;
}

.stButton>button {
    background: linear-gradient(90deg, #00f5a0, #00d9f5);
    border-radius: 12px;
    color: black;
    font-weight: bold;
    height: 48px;
}
</style>
""", unsafe_allow_html=True)

st.title("💪 AI Fitness Trainer")

# =========================
# FUNCTIONS
# =========================
def height_cm(f, i):
    return f*30.48 + i*2.54

def bmi_calc(w, h):
    return round(w / ((h/100)**2), 2)

def bmi_type(b):
    if b < 18.5: return "Underweight"
    elif b < 25: return "Normal"
    elif b < 30: return "Overweight"
    else: return "Obese"

def bmr(w, h, a):
    return 10*w + 6.25*h - 5*a + 5

def tdee_calc(bmr, act):
    return bmr * (1.2 if act=="Low" else 1.55 if act=="Moderate" else 1.725)

def goal_cal(tdee, goal):
    return int(tdee + 400 if goal=="Bulk" else tdee - 400 if goal=="Cut" else tdee)

def smart_plan(goal, bmi_cat):
    if bmi_cat == "Underweight":
        return "💪 Bulking Focus (Calorie Surplus + Strength Training)"
    elif bmi_cat in ["Overweight", "Obese"]:
        return "🔥 Fat Loss Focus (Cardio + Calorie Deficit)"
    else:
        return f"⚖️ Balanced Fitness Plan for {goal}"

def water_intake(weight, activity):
    base = weight * 0.035
    if activity == "Moderate":
        base += 0.5
    elif activity == "High":
        base += 1.0
    return round(base, 2)

def workout_split(goal):
    if goal == "Bulk":
        return ["Chest + Triceps", "Back + Biceps", "Legs", "Shoulders", "Repeat"]
    elif goal == "Cut":
        return ["HIIT + Abs", "Upper Body", "Cardio", "Lower Body", "Core"]
    else:
        return ["Full Body", "Rest/Cardio", "Upper", "Lower", "Light Training"]

# =========================
# 🍱 DIET (Veg/Non-Veg + Health Safe)
# =========================
def meal_plan(cal, goal, pref, health):

    protein = int(cal * 0.3 / 4)

    breakfast = {
        "Veg": ["Oats + Milk + Banana", "Idli + Sambar", "Upma", "Poha",
                "Paneer Sandwich", "Peanut Butter Toast"],
        "Non-Veg": ["Oats + Eggs", "Egg Omelette + Bread",
                    "Boiled Eggs + Toast", "Chicken Sandwich"]
    }

    lunch = {
        "Veg": ["Rice + Dal + Ghee", "Paneer + Chapati",
                "Rajma + Rice", "Veg Biryani (low oil)"],
        "Non-Veg": ["Chicken Curry + Rice", "Fish Curry + Rice",
                    "Chicken Biryani (controlled)", "Grilled Chicken + Rice"]
    }

    dinner = {
        "Veg": ["Chapati + Veg", "Paneer + Roti",
                "Dal + Rice", "Veg Soup + Salad"],
        "Non-Veg": ["Chicken + Chapati", "Fish + Rice",
                    "Eggs + Roti", "Grilled Chicken + Salad"]
    }

    snacks = {
        "Veg": ["Fruits", "Nuts", "Buttermilk",
                "Protein Shake", "Peanut Butter Sandwich"],
        "Non-Veg": ["Boiled Eggs", "Chicken Salad",
                    "Protein Shake", "Greek Yogurt"]
    }

    # 🔒 Health-based filtering
    if health == "Diabetes":
        breakfast[pref] = [x for x in breakfast[pref] if "Banana" not in x]
        snacks[pref] = [x for x in snacks[pref] if "Shake" not in x]

    elif health == "High BP":
        lunch[pref] = [x for x in lunch[pref] if "Biryani" not in x]
        dinner[pref] = [x for x in dinner[pref] if "Biryani" not in x]

    elif health == "Sensitive Digestion":
        breakfast[pref] = [x for x in breakfast[pref] if "Paratha" not in x]
        lunch[pref] = [x for x in lunch[pref] if "Biryani" not in x]

    def pick(meals):
        return random.sample(meals, 1)[0]

    return [
        f"🥞 Breakfast: {pick(breakfast[pref])}",
        f"🍛 Lunch: {pick(lunch[pref])}",
        f"🍲 Dinner: {pick(dinner[pref])}",
        f"🥤 Snacks: {pick(snacks[pref])}",
        f"💪 Protein: {protein}g"
    ]

# =========================
# LAYOUT
# =========================
col1, col2 = st.columns([1,2])

with col1:
    st.subheader("📝 Enter Details")

    weight = st.number_input("⚖️ Weight (kg)", 30,150)

    c1, c2 = st.columns(2)
    with c1:
        feet = st.number_input("📏 Feet",3,7)
    with c2:
        inches = st.number_input("📏 Inches",0,11)

    age = st.number_input("🎂 Age",15,60)

    activity = st.selectbox("🏃 Activity Level", ["Low","Moderate","High"])
    goal = st.selectbox("🎯 Goal", ["Bulk","Cut","Maintain"])

    diet_pref = st.selectbox("🍽️ Diet Preference", ["Veg","Non-Veg"])

    # ✅ NEW HEALTH OPTION
    health = st.selectbox("🩺 Health Condition", ["None", "Diabetes", "High BP", "Sensitive Digestion"])

    generate = st.button("🚀 Generate Plan")

# =========================
# OUTPUT
# =========================
with col2:
    if generate:
        with st.spinner("⚡ Generating AI Plan..."):
            time.sleep(1.5)

        h = height_cm(feet, inches)
        bmi = bmi_calc(weight, h)
        cat = bmi_type(bmi)

        b = bmr(weight, h, age)
        t = tdee_calc(b, activity)
        cal = goal_cal(t, goal)

        water = water_intake(weight, activity)

        st.markdown(f'<div class="card"><div class="card-title">🧠 AI Insight</div>{smart_plan(goal,cat)}</div>', unsafe_allow_html=True)

        st.markdown(f'<div class="card"><div class="card-title">📊 Body Stats</div>BMI: {bmi} ({cat})<br>Calories: {cal}<br>Water: {water}L 💧</div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">🏋️ Workout Plan</div>', unsafe_allow_html=True)
        for d in workout_split(goal):
            st.write("👉", d)
        st.markdown('</div>', unsafe_allow_html=True)

        meals = meal_plan(cal, goal, diet_pref, health)

        st.markdown('<div class="card"><div class="card-title">🍱 Diet Plan</div>', unsafe_allow_html=True)
        for m in meals:
            st.write("👉", m)
        st.markdown('</div>', unsafe_allow_html=True)
