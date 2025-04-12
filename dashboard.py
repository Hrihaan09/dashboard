import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📚 Tutoring Performance Dashboard")
st.markdown("Upload your CSV file below to generate your custom dashboard.")

# File upload
uploaded_file = st.file_uploader("📁 Upload your data file (.csv)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    try:
        # Show raw data
        st.subheader("🧾 Uploaded Data Preview")
        st.write(df.head())

        # Filter by student
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

    except Exception as e:
        st.error(f"⚠️ Error processing file: {e}")
        st.info("Make sure your file has the following columns: Student, Subject, Date, Score, Attended")

else:
    st.info("⬆️ Please upload a CSV file to get started.")
