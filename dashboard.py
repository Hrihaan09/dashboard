import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.express as px

# Set up Google Sheets API credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Load data from Google Sheet
sheet = client.open("Dashboard Sample Data").sheet1  # <-- change this to the name of your Google Sheet
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Streamlit Dashboard
st.title("📚 Tutoring Performance Dashboard")
st.markdown("Visualize student performance and attendance from your spreadsheet.")

# Student filter
students = df['Student'].unique()
selected_student = st.selectbox("Select a student", students)
student_df = df[df['Student'] == selected_student]

# Score trend
st.subheader("📈 Score Over Time")
fig1 = px.line(student_df, x='Date', y='Score', color='Subject', markers=True)
st.plotly_chart(fig1)

# Attendance bar chart
st.subheader("✅ Attendance by Subject")
attendance_summary = student_df.groupby('Subject')['Attended'].sum().reset_index()
fig2 = px.bar(attendance_summary, x='Subject', y='Attended', color='Subject')
st.plotly_chart(fig2)

# Average scores
st.subheader("📊 Average Score by Subject")
avg_scores = student_df.groupby('Subject')['Score'].mean().reset_index()
fig3 = px.bar(avg_scores, x='Subject', y='Score', color='Subject')
st.plotly_chart(fig3)
