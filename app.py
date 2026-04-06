import streamlit as st
import json
from datetime import datetime

# -------- CONFIG & DATA --------
st.set_page_config(page_title="Student Psychological Survey")

if 'survey_started' not in st.session_state:
    st.session_state.survey_started = False

version_float = 1.1

# Fixed typos in your questions (Rareky -> Rarely, Oftern -> Often)
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
def validate_name(name: str) -> bool:
    return len(name.strip()) > 0 and not any(c.isdigit() for c in name)

def interpret_score(score: int) -> str:
    for state, (low, high) in psych_states.items():
        if low <= score <= high:
            return state
    return "Unknown"

# ---------------- STREAMLIT APP ----------------
st.title("📝 Student Psychological Survey")
st.info("Please fill out your details and answer all questions honestly.")

# --- User Info ---
# Using columns to make it look cleaner
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Given Name")
    surname = st.text_input("Surname")
with col2:
    dob = st.date_input("Date of Birth", value=None, min_value=datetime(1900, 1, 1)) # Better than text_input
    sid = st.text_input("Student ID (digits only)")

# --- Control Logic ---
if st.button("Start Survey"):
    errors = []
    if not validate_name(name): errors.append("Invalid given name.")
    if not validate_name(surname): errors.append("Invalid surname.")
    if not dob: errors.append("Please select a valid date of birth.")
    if not sid.isdigit(): errors.append("Student ID must be digits only.")

    if errors:
        for e in errors: st.error(e)
    else:
        st.session_state.survey_started = True

# --- The Survey Section ---
if st.session_state.survey_started:
    st.divider()
    # Using st.form prevents the page from refreshing after every single click
    with st.form("survey_form"):
        st.subheader("Survey Questions")
        user_answers = []
        
        for idx, q in enumerate(questions):
            opt_labels = [opt[0] for opt in q["opts"]]
            choice = st.selectbox(f"Q{idx+1}. {q['q']}", opt_labels, key=f"q{idx}")
            user_answers.append((choice, q))

        submit_survey = st.form_submit_button("Submit Results")

        if submit_survey:
            total_score = 0
            final_answers = []

            for choice, q in user_answers:
                score = next(score for label, score in q["opts"] if label == choice)
                total_score += score
                final_answers.append({"question": q["q"], "selected_option": choice, "score": score})

            status = interpret_score(total_score)
            
            st.success("Survey Submitted!")
            st.markdown(f"## ✅ Your Result: {status}")
            st.markdown(f"**Total Score:** {total_score}")

            # Save results
            record = {
                "name": name, "surname": surname, "dob": str(dob),
                "student_id": sid, "total_score": total_score,
                "result": status, "answers": final_answers, "version": version_float
            }
            
            json_filename = f"{sid}_result.json"
            st.download_button("Download Result JSON", json.dumps(record, indent=2), file_name=json_filename)