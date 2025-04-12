import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("data.csv", parse_dates=['Date'])

st.title("📚 Tutoring Performance Dashboard")
st.markdown("This dashboard shows student performance and attendance over time.")

# Filter by student
student_list = df['Student'].unique()
selected_student = st.selectbox("Select a student", student_list)

student_data = df[df['Student'] == selected_student]

# Score Trend
st.subheader("📈 Score Over Time")
fig = px.line(student_data, x='Date', y='Score', color='Subject', markers=True)
st.plotly_chart(fig)

# Attendance Overview
st.subheader("✅ Attendance Record")
attendance_count = student_data.groupby('Subject')['Attended'].sum().reset_index()
fig2 = px.bar(attendance_count, x='Subject', y='Attended', color='Subject')
st.plotly_chart(fig2)

# Average Score by Subject
st.subheader("📊 Average Score by Subject")
avg_scores = student_data.groupby('Subject')['Score'].mean().reset_index()
fig3 = px.bar(avg_scores, x='Subject', y='Score', color='Subject')
st.plotly_chart(fig3)
