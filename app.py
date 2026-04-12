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
# 🇮🇳 DYNAMIC DIET
# =========================
def meal_plan(cal, goal):

    protein = int(cal * 0.3 / 4)

    breakfast_bulk = ["Oats + Milk + Banana", "Idli + Sambar + Eggs", "Dosa + Milk", "Paratha + Curd"]
    lunch_bulk = ["Rice + Chicken Curry", "Rice + Dal + Ghee", "Biryani + Raita", "Chapati + Paneer"]
    dinner_bulk = ["Chapati + Eggs", "Rice + Fish Curry", "Paneer + Roti", "Chicken + Chapati"]
    snacks_bulk = ["Banana Shake", "Dry Fruits", "Peanut Butter Sandwich", "Lassi"]

    breakfast_cut = ["Oats + Fruits", "Idli (2)", "Boiled Eggs + Apple", "Upma"]
    lunch_cut = ["Grilled Chicken + Salad", "Dal + Veg", "Paneer + Salad", "Rice (small) + Dal"]
    dinner_cut = ["Boiled Eggs + Veg", "Soup + Salad", "Chicken + Veg", "Paneer + Salad"]
    snacks_cut = ["Sprouts", "Buttermilk", "Fruits", "Green Tea"]

    breakfast_bal = ["Upma + Milk", "Eggs + Toast", "Idli + Sambar", "Oats + Fruits"]
    lunch_bal = ["Rice + Dal + Veg", "Chapati + Chicken", "Rice + Paneer", "Curd Rice"]
    dinner_bal = ["Chapati + Veg", "Eggs + Salad", "Light Rice + Dal", "Paneer + Roti"]
    snacks_bal = ["Fruits", "Nuts", "Buttermilk", "Boiled Corn"]

    if goal == "Bulk":
        return [
            f"🥞 Breakfast: {random.choice(breakfast_bulk)}",
            f"🍛 Lunch: {random.choice(lunch_bulk)}",
            f"🍲 Dinner: {random.choice(dinner_bulk)}",
            f"🥤 Snacks: {random.choice(snacks_bulk)}",
            f"💪 Protein: {protein}g"
        ]

    elif goal == "Cut":
        return [
            f"🥗 Breakfast: {random.choice(breakfast_cut)}",
            f"🍗 Lunch: {random.choice(lunch_cut)}",
            f"🥚 Dinner: {random.choice(dinner_cut)}",
            f"🥒 Snacks: {random.choice(snacks_cut)}",
            f"🔥 Protein: {protein}g"
        ]

    else:
        return [
            f"🍞 Breakfast: {random.choice(breakfast_bal)}",
            f"🍛 Lunch: {random.choice(lunch_bal)}",
            f"🥗 Dinner: {random.choice(dinner_bal)}",
            f"🥜 Snacks: {random.choice(snacks_bal)}",
            f"⚖️ Protein: {protein}g"
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

        meals = meal_plan(cal, goal)
        st.markdown('<div class="card"><div class="card-title">🍱 Diet Plan</div>', unsafe_allow_html=True)
        for m in meals:
            st.write("👉", m)
        st.markdown('</div>', unsafe_allow_html=True)