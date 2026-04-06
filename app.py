import streamlit as st
import json
from datetime import datetime

# -------- INITIALIZATION --------
st.set_page_config(page_title="Student Psychological Survey")

# 1. Create a "memory" for the app so it knows the survey is active
if 'survey_started' not in st.session_state:
    st.session_state.survey_started = False

# -------- DATA --------
version_float = 1.1
questions = [
    {"q": "How many hours per day do you spend on your smartphone?",
     "opts": [("Less than 1 hour",0),("1-2 hours",1),("3-4 hours",2),("5-6 hours",3),("More than 6 hours",4)]},
    {"q": "How often do you check your phone immediately after waking up?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    # ... (Include all your other questions here)
]

psych_states = {
    "Very Healthy Digital Habits": (0, 10),
    "Mostly Healthy Use": (11, 20),
    "Mild Digital Strain": (21, 30),
    "Moderate Digital Stress": (31, 40),
    "High Digital Overload": (41, 50),
    "Severe Digital Burnout Risk": (51, 60),
}

def interpret_score(score: int) -> str:
    for state, (low, high) in psych_states.items():
        if low <= score <= high: return state
    return "Unknown"

# -------- UI --------
st.title("📝 Student Psychological Survey")

# User Details
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Given Name")
    surname = st.text_input("Surname")
with col2:
    dob = st.date_input("Date of Birth", value=None) # Better than text_input
    sid = st.text_input("Student ID (digits only)")

# 2. Trigger the survey state
if st.button("Start Survey"):
    if name and surname and dob and sid.isdigit():
        st.session_state.survey_started = True
    else:
        st.error("Please fill in all personal details first.")

# 3. Only show the survey if the state is "True"
if st.session_state.survey_started:
    st.divider()
    
    # Use a Form so it doesn't refresh until the user clicks "Submit"
    with st.form("my_survey_form"):
        st.subheader("Please answer the following:")
        user_responses = []
        
        for idx, q in enumerate(questions):
            labels = [opt[0] for opt in q["opts"]]
            choice = st.selectbox(f"Q{idx+1}. {q['q']}", labels, key=f"q_{idx}")
            user_responses.append((choice, q))

        submit_btn = st.form_submit_button("Submit Survey")

        if submit_btn:
            total_score = 0
            for choice, q in user_responses:
                score = next(s for label, s in q["opts"] if label == choice)
                total_score += score
            
            result = interpret_score(total_score)
            st.success(f"Done! Your result: {result} (Score: {total_score})")
            
            # (Your logic for saving JSON goes here)
