import streamlit as st
import json
from datetime import datetime

# -------- 1. INITIALIZATION & SESSION STATE --------
# This prevents the survey from disappearing when you interact with widgets.
if 'survey_started' not in st.session_state:
    st.session_state.survey_started = False

st.set_page_config(page_title="Student Psychological Survey")

version_float = 1.1

# -------- 2. SURVEY DATA --------
# Typos like "Rareky" and "Oftern" have been corrected.
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

# -------- 3. HELPERS --------
def interpret_score(score: int) -> str:
    for state, (low, high) in psych_states.items():
        if low <= score <= high:
            return state
    return "Unknown"

# -------- 4. MAIN APP UI --------
st.title("📝 Student Psychological Survey")
st.info("Please fill out your details and answer all questions honestly.")

# User Info inputs
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Given Name")
    surname = st.text_input("Surname")
with col2:
    # date_input is more reliable for web apps than text_input.
    dob = st.date_input("Date of Birth", value=None, min_value=datetime(1900, 1, 1))
    sid = st.text_input("Student ID (digits only)")

# Start button sets the session state to True
if st.button("Start Survey"):
    if name and surname and dob and sid.isdigit():
        st.session_state.survey_started = True
    else:
        st.error("Please fill in all details correctly before starting.")

# -------- 5. SURVEY LOGIC --------
if st.session_state.survey_started:
    st.divider()
    
    # Use a form to prevent the app from refreshing after every single choice.
    with st.form("survey_form"):
        st.subheader("Questions")
        temp_answers = []
        
        for idx, q in enumerate(questions):
            opt_labels = [opt[0] for opt in q["opts"]]
            choice = st.selectbox(f"Q{idx+1}. {q['q']}", opt_labels, key=f"q{idx}")
            temp_answers.append((choice, q))
            
        # The submit button inside the form
        submitted = st.form_submit_button("Submit Survey")

    # Processing occurs OUTSIDE the form to allow the download button to work.
    if submitted:
        total_score = 0
        final_answers = []

        for choice, q in temp_answers:
            score = next(s for label, s in q["opts"] if label == choice)
            total_score += score
            final_answers.append({
                "question": q["q"],
                "selected_option": choice,
                "score": score
            })

        status = interpret_score(total_score)

        st.success("Results processed successfully!")
        st.markdown(f"## ✅ Your Result: {status}")
        st.markdown(f"**Total Score:** {total_score}")

        # Create the result record
        record = {
            "name": name,
            "surname": surname,
            "dob": str(dob),
            "student_id": sid,
            "total_score": total_score,
            "result": status,
            "answers": final_answers,
            "version": version_float
        }

        # The download button must be outside the st.form block.
        st.download_button(
            label="📥 Download Your Result (JSON)",
            data=json.dumps(record, indent=2),
            file_name=f"{sid}_result.json",
            mime="application/json"
        )
