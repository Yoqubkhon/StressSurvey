import streamlit as st
import json
from datetime import datetime

# --- 1. SESSION STATE INITIALIZATION ---
# This acts as the "memory" of your app so the survey doesn't disappear.
if 'survey_started' not in st.session_state:
    st.session_state.survey_started = False

# --- 2. DATA & CONFIG ---
st.set_page_config(page_title="Student Psychological Survey", layout="centered")

version_float = 1.1

# I fixed the typos in your options (Rareky -> Rarely, Oftern -> Often)
questions = [
    {"q": "How many hours per day do you spend on your smartphone?",
     "opts": [("Less than 1 hour",0),("1-2 hours",1),("3-4 hours",2),("5-6 hours",3),("More than 6 hours",4)]},
    {"q": "How often do you check your phone immediately after waking up?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "Do you use your smartphone during lectures or study time?", 
     "opts": [("Never", 0),("Rarely", 1),("Sometimes", 2),("Often", 3),("Always",4)]},
    {"q": "How often do notifications distract you from tasks?",
     "opts": [("Never", 0),("Rarely", 1),("Sometimes", 2),("Often", 3),("Always",4)]},
    {"q": "How frequently do you use your phone after midnight?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Every Night",4)]},
    {"q": "Do you feel tired in the morning due to late-night phone use?", 
     "opts": [("Never", 0),("Rarely", 1),("Sometimes", 2),("Often", 3),("Always",4)]},
    {"q": "How often do you postpone sleep because of social media?",
     "opts": [("Never", 0),("Rarely", 1),("Sometimes", 2),("Often", 3),("Always",4)]},
    {"q": "Do you feel anxious when you cannot access your phone?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "How often does phone usage interfere with your academic work?", 
     "opts": [("Never", 0),("Rarely", 1),("Sometimes", 2),("Often", 3),("Always",4)]},
    {"q": "How frequently do you feel mentally exhausted after long screen time?",
     "opts": [("Never", 0),("Rarely", 1),("Sometimes", 2),("Often", 3),("Always",4)]},
    {"q": "Do you feel more stressed after browsing social media?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "How often do you lose track of time while using apps?", 
     "opts": [("Never", 0),("Rarely", 1),("Sometimes", 2),("Often", 3),("Always",4)]},
    {"q": "Do you feel pressure to respond quickly to messages?",
     "opts": [("Never", 0),("Rarely", 1),("Sometimes", 2),("Often", 3),("Always",4)]},
    {"q": "How often do you compare yourself to others online?", 
     "opts": [("Never", 0),("Rarely", 1),("Sometimes", 2),("Often", 3),("Always",4)]},
    {"q": "Do you feel relaxed after spending time offline?",
     "opts": [("Always", 0),("Often", 1),("Sometimes", 2),("Rarely", 3),("Never",4)]}
]

psych_states = {
    "Very Healthy Digital Habits": (0, 10),
    "Mostly Healthy Use": (11, 20),
    "Mild Digital Strain": (21, 30),
    "Moderate Digital Stress": (31, 40),
    "High Digital Overload": (41, 50),
    "Severe Digital Burnout Risk": (51, 60),
}

# --- 3. HELPERS ---
def interpret_score(score: int) -> str:
    for state, (low, high) in psych_states.items():
        if low <= score <= high: return state
    return "Unknown"

# --- 4. APP UI ---
st.title("📝 Student Psychological Survey")
st.markdown("---")

# User Details (Persistent outside the survey logic)
st.subheader("Step 1: Personal Information")
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Given Name")
    surname = st.text_input("Surname")
with col2:
    dob = st.date_input("Date of Birth", value=None, min_value=datetime(1900, 1, 1))
    sid = st.text_input("Student ID (digits only)")

# Start Survey Button
if not st.session_state.survey_started:
    if st.button("Unlock Survey"):
        if name and surname and dob and sid.isdigit():
            st.session_state.survey_started = True
            st.rerun()
        else:
            st.error("Please provide all details correctly before starting.")

# --- 5. THE SURVEY SECTION ---
if st.session_state.survey_started:
    st.success("Information Verified. Please complete the survey below.")
    
    # Using st.form prevents the app from refreshing every time you pick an answer
    with st.form("survey_questions"):
        st.subheader("Step 2: Questionnaire")
        user_responses = []

        for idx, q_data in enumerate(questions):
            options = [opt[0] for opt in q_data["opts"]]
            choice = st.selectbox(f"Q{idx+1}. {q_data['q']}", options, key=f"q_{idx}")
            user_responses.append((choice, q_data))

        # The actual submission button
        submit_survey = st.form_submit_button("Finish & Get Results")

        if submit_survey:
            total_score = 0
            answered_data = []

            for choice, q_data in user_responses:
                # Find score of the selected label
                score = next(s for label, s in q_data["opts"] if label == choice)
                total_score += score
                answered_data.append({
                    "question": q_data["q"],
                    "selected_option": choice,
                    "score": score
                })

            status = interpret_score(total_score)

            # Show Results
            st.divider()
            st.balloons()
            st.markdown(f"## ✅ Your Status: **{status}**")
            st.metric("Total Score", total_score)

            # JSON Record
            record = {
                "name": name, "surname": surname, "dob": str(dob), "student_id": sid,
                "total_score": total_score, "result": status,
                "answers": answered_data, "version": version_float
            }

            # Download Button
            st.download_button(
                label="📥 Download Result (JSON)",
                data=json.dumps(record, indent=2),
                file_name=f"{sid}_survey_result.json",
                mime="application/json"
            )
