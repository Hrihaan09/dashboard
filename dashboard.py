import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Smart Business Dashboard")
st.markdown("Upload a CSV with your business data — we'll analyze it for you automatically.")

uploaded_file = st.file_uploader("📁 Upload your .csv file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.subheader("🧾 Data Preview")
        st.write(df.head())

        # Show column types
        st.subheader("🔍 Column Type Detection")
        st.write(df.dtypes)

        # Dropdowns for user to select important columns
        date_col = st.selectbox("Select a date column (optional)", options=["None"] + list(df.columns))
        category_col = st.selectbox("Select a category column (optional)", options=["None"] + list(df.columns))
        numeric_col = st.selectbox("Select a numeric column to analyze", options=df.select_dtypes(include='number').columns)

        # Chart: Numeric over time
        if date_col != "None":
            st.subheader(f"📈 {numeric_col} Over Time")
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            fig1 = px.line(df, x=date_col, y=numeric_col)
            st.plotly_chart(fig1)

        # Chart: Category breakdown
        if category_col != "None":
            st.subheader(f"📊 {numeric_col} by {category_col}")
            grouped = df.groupby(category_col)[numeric_col].mean().reset_index()
            fig2 = px.bar(grouped, x=category_col, y=numeric_col, color=category_col)
            st.plotly_chart(fig2)

        # Summary stats
        st.subheader(f"📌 Summary of {numeric_col}")
        st.write(df[numeric_col].describe())

    except Exception as e:
        st.error(f"❌ Something went wrong: {e}")
else:
    st.info("⬆️ Upload a CSV to get started")
