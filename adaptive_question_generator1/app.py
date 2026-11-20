import streamlit as st
import json
import os
from agent import generate_questions
from adaptive_engine import get_next_difficulty

st.set_page_config(page_title="AI Adaptive Quiz", page_icon="🎓")

# ---------- Session ----------
if "quiz" not in st.session_state:
    st.session_state.quiz = None
if "index" not in st.session_state:
    st.session_state.index = 0
if "answers" not in st.session_state:
    st.session_state.answers = []
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "student" not in st.session_state:
    st.session_state.student = ""
if "subject" not in st.session_state:
    st.session_state.subject = ""
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "score" not in st.session_state:
    st.session_state.score = 0
if "total" not in st.session_state:
    st.session_state.total = 0
if "percent" not in st.session_state:
    st.session_state.percent = 0

# ---------- Save Result ----------
def save_result():
    data = []
    if os.path.exists("results.json"):
        with open("results.json","r") as f:
            data = json.load(f)

    data.append({
        "student": st.session_state.student,
        "subject": st.session_state.subject,
        "topic": st.session_state.topic,
        "score": st.session_state.score,
        "total": st.session_state.total,
        "percentage": st.session_state.percent
    })

    with open("results.json","w") as f:
        json.dump(data,f,indent=4)

# ---------- Home ----------
st.title("🎓 AI Adaptive Question Generator")

if st.session_state.quiz is None:

    name = st.text_input("Student Name")
    subject = st.selectbox("Subject",["Python","AI","ML","DBMS"])
    topic = st.text_input("Topic")
    difficulty = st.selectbox("Difficulty",["Easy","Medium","Hard"])
    number = st.slider("Questions",1,10,5)

    if st.button("Generate Quiz"):

        quiz = generate_questions(subject,topic,difficulty,number)

        st.session_state.quiz = quiz
        st.session_state.answers = [None]*len(quiz)

        # SAVE STUDENT DETAILS
        st.session_state.student = name
        st.session_state.subject = subject
        st.session_state.topic = topic

        st.rerun()

# ---------- Quiz ----------
elif not st.session_state.submitted:

    q = st.session_state.quiz[st.session_state.index]

    st.subheader(f"Question {st.session_state.index+1}/{len(st.session_state.quiz)}")
    st.write(q["question"])

    choice = st.radio(
        "Select Answer",
        q["options"],
        index=None,
        key=f"q{st.session_state.index}"
    )

    if choice:
        st.session_state.answers[st.session_state.index] = choice

    c1,c2 = st.columns(2)

    with c1:
        if st.session_state.index>0:
            if st.button("Previous"):
                st.session_state.index -=1
                st.rerun()

    with c2:
        if st.session_state.index < len(st.session_state.quiz)-1:
            if st.button("Next"):
                st.session_state.index +=1
                st.rerun()
        else:
            if st.button("Submit Quiz"):

                score = 0

                for i,item in enumerate(st.session_state.quiz):
                    if st.session_state.answers[i] == item["answer"]:
                        score +=1

                total = len(st.session_state.quiz)
                percent = round(score/total*100)

                st.session_state.score = score
                st.session_state.total = total
                st.session_state.percent = percent
                st.session_state.submitted = True

                save_result()

                st.rerun()

# ---------- Result ----------
else:

    st.balloons()

    st.title("🏆 Quiz Result")

    st.write(f"## 👤 Student : {st.session_state.student}")
    st.write(f"**Subject :** {st.session_state.subject}")
    st.write(f"**Topic :** {st.session_state.topic}")

    st.metric("Score",f"{st.session_state.score}/{st.session_state.total}")

    st.progress(st.session_state.percent/100)

    st.success(f"{st.session_state.percent}%")

    next_level = get_next_difficulty(st.session_state.percent)
    st.info(f"Next Difficulty : {next_level}")

    if st.button("Start New Quiz"):
        st.session_state.quiz = None
        st.session_state.index = 0
        st.session_state.answers = []
        st.session_state.submitted = False
        st.rerun()