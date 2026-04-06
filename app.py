import streamlit as st
import json
from datetime import datetime

# -------- CONFIG & SESSION STATE --------
st.set_page_config(page_title="Student Psychological Survey")

# This is the "memory" logic. If it doesn't exist, create it.
if 'survey_started' not in st.session_state:
    st.session_state.survey_started = False

version_float = 1.1

# -------- QUESTIONS (Typos Fixed) --------
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

# ---------------- HELPERS ----------------
def interpret_score(score: int) -> str:
    for state, (low, high) in psych_states.items():
        if low <= score <= high:
            return state
    return "Unknown"

# ---------------- STREAMLIT APP ----------------
st.title("📝 Student Psychological Survey")
st.info("Fill out your details and click 'Start Survey' to begin.")

# --- User Info ---
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Given Name", key="name_input")
    surname = st.text_input("Surname", key="surname_input")
with col2:
    # Using date_input is safer than text_input for dates
    dob = st.date_input("Date of Birth", value=None, min_value=datetime(1900, 1, 1))
    sid = st.text_input("Student ID (digits only)", key="sid_input")

# --- Logic to Start the Survey ---
if st.button("Start Survey"):
    if name and surname and dob and sid.isdigit():
        st.session_state.survey_started = True
    else:
        st.error("Please fill in all fields correctly (ensure Student ID is digits only).")

# --- The Survey Section ---
# This part only shows if st.session_state.survey_started is True
if st.session_state.survey_started:
    st.divider()
    
    # We use a form so the app doesn't reset after every answer selected
    with st.form("survey_form"):
        st.subheader("Questionnaire")
        
        # Store questions in a dictionary so we can retrieve them after submit
        current_responses = []
        
        for idx, q in enumerate(questions):
            opt_labels = [opt[0] for opt in q["opts"]]
            user_choice = st.selectbox(f"Q{idx+1}. {q['q']}", opt_labels, key=f"q_{idx}")
            current_responses.append((user_choice, q))

        # The actual submit button for the form
        submit_survey = st.form_submit_button("Complete Survey & See Result")

        if submit_survey:
            total_score = 0
            answers_json = []

            for choice, q_data in current_responses:
                # Find the score for the selected text
                score = next(s for label, s in q_data["opts"] if label == choice)
                total_score += score
                answers_json.append({
                    "question": q_data["q"],
                    "selected_option": choice,
                    "score": score
                })

            status = interpret_score(total_score)

            # --- Results Display ---
            st.balloons()
            st.markdown(f"## ✅ Your Result: {status}")
            st.markdown(f"**Total Score:** {total_score}")

            # --- Save & Download ---
            record = {
                "name": name,
                "surname": surname,
                "dob": str(dob),
                "student_id": sid,
                "total_score": total_score,
                "result": status,
                "answers": answers_json,
                "version": version_float
            }

            st.download_button(
                label="Download Your Result (JSON)",
                data=json.dumps(record, indent=2),
                file_name=f"{sid}_result.json",
                mime="application/json"
            )
