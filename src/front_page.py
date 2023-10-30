from pathlib import Path
import pandas as pd
import streamlit as st
import sys
import os
import plotly.express as plt

sys.path.insert(0, os.path.join(Path(__file__).parents[0]))
from mongo_conn import MongoConn

sg = MongoConn()

df = pd.DataFrame(list(sg.student_grades.find({})))

st.title("Student Grades Evaluation")
st.text(
    """
    Examining factors in Portugese secondary school students 
    with an aim to identify students requiring additional support.
"""
)

st.sidebar.title("Data Overview")

student_group = st.sidebar.radio(
    "Which subject to examine?", ["Math", "Portugese", "Both"]
)

if student_group == "Math":
    show_data = df[df["subj"] == "mat"]
elif student_group == "Portugese":
    show_data = df[df["subj"] == "por"]
else:
    show_data = df

st.sidebar.subheader("Variables Surveyed:")
st.sidebar.markdown(
    "**School:** GP/MS  \n **Age:** Numeric Age:  \n **Address:** Urban/Rural  \n **FamSize:** Family Size Under/Over 3  \n **M_Edu:** Mother's Education  \n **F_Edu:** Father's Education  \n  **M_Job:** Mother's Job  \n  **F_Job:** Father's Job  \n **Reason:** Factor Determining School Choice  \n  **Guardian:** Primary Guardian  \n **TravelTime:** Travel Time (to school)  \n **StudyTime:** Hours Weekly Study  \n **Failures:** Failed Classes  \n **SchoolSup:** Extra Education Support (T/F)  \n **FamSup:** Family Educational Support (T/F)  \n **Paid:** Paid Classes/Tutoring in Subject (T/F)  \n **Activities:** Extracirricular Activities (T/F)   \n **Nursery:** Attended PreSchool (T/F)  \n **Higher:** Wants To Attend College: (T/F)  \n **Internet:** Internet At Home: (T/F)  \n **Romantic:** Romantically Involved (T/F)   \n **FamRel:** Self-Rated 1-5  \n **FreeTime:** Free Time Self-Rated 1-5  \n**GoOut:** Social Life Self-Rated 1-5  \n **D_Alc:** Weekday Alcohol Use, Self-Rated 1-5  \n **W_Alc:** Weekend Alcohol Use, Self-Rated 1-5  \n **Health** Health Self-Rated 1-5  \n **Absences:** Days Absent  \n **G_1:** First Period Grade (0-20)  \n **G_2:** Second Period Grade (0-20)  \n **G_3:** Final Grade (0-20)"
)

vis_to_use = ["scatterplot", "histogram", "pie"]
type_vis = st.selectbox(
    "select the type of visualization you would like to see", options=vis_to_use
)

if type_vis == "scatterplot":
    st.text("Suggested columns: Absences, Age, Failures, G_1-G_3, Study Time")
    st.text("...or any self-rating category such as Free Time or Health")

    answer_x = st.selectbox(
        "select a column to visualize on the x axis", options=list(show_data.columns)
    )
    answer_y = st.selectbox(
        "select a column to visualize on the y axis", options=list(show_data.columns)
    )
    if answer_x and answer_y:
        try:
            st.plotly_chart(
                plt.scatter(show_data, x=answer_x, y=answer_y), use_container_width=True
            )
        except BaseException:
            print("error visualizing that combination of columns")

elif type_vis == "histogram":
    answer = st.selectbox(
        "select a column to visualize", options=list(show_data.columns)
    )
    answer_c = st.radio(
        "How to colorize the results? (Subj is also selected in the sidebar)",
        ["age", "school", "subj", "address"],
    )
    if answer:
        try:
            st.plotly_chart(
                plt.histogram(show_data, x=answer, color=answer_c),
                use_container_width=True,
            )
        except BaseException:
            print("error visualizing that combination of columns")

elif type_vis == "pie":
    st.text("now's a good time to investigate those T/F columns")
    answer = st.selectbox(
        "select a column to visualize", options=list(show_data.columns)
    )

    if answer:
        pie_prep = show_data[answer].value_counts()
        pie_format = pd.DataFrame(pie_prep).reset_index()
        if len(pie_format) > 5:
            st.text("Not a good column for that, pick another!")
        try:
            st.plotly_chart(
                plt.pie(pie_format, values="count", names=answer),
                use_container_width=True,
            )
        except BaseException:
            print("error visualizing that combination of columns")
