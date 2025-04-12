import streamlit as st
import pandas as pd
import plotly.express as px

# App title and intro
st.set_page_config(page_title="SmartBiz Dashboard", layout="wide")
st.title("📊 SmartBiz Dashboard")
st.markdown("""
Welcome! Upload your **CSV business data** and get an instant dashboard.

ℹ️ Your file should include at least:
- One **date** column
- One **numeric** column (like sales, revenue, or customers)
- Optional **category** column (like service, product, employee, etc.)
""")

# Sidebar: Upload file
st.sidebar.header("📁 Upload CSV File")
uploaded_file = st.sidebar.file_uploader("Upload your file", type=["csv"])

# If a file is uploaded
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        st.subheader("🧾 Data Preview")
        st.dataframe(df.head())

        # Sidebar: Column selectors
        st.sidebar.header("🔧 Select Columns")
        date_col = st.sidebar.selectbox("📅 Date Column", options=["None"] + list(df.columns))
        numeric_col = st.sidebar.selectbox("🔢 Numeric Column (e.g. revenue)", options=df.select_dtypes(include='number').columns)
        category_col = st.sidebar.selectbox("🏷️ Category Column (optional)", options=["None"] + list(df.columns))

        if date_col != "None":
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

        # Charts
        st.markdown("## 📈 Dashboard")

        col1, col2 = st.columns(2)

        if date_col != "None":
            with col1:
                st.markdown(f"### 🔄 {numeric_col} Over Time")
                fig = px.line(df, x=date_col, y=numeric_col, title=f"{numeric_col} Trend")
                st.plotly_chart(fig, use_container_width=True)

        if category_col != "None":
            with col2:
                st.markdown(f"### 📊 {numeric_col} by {category_col}")
                grouped = df.groupby(category_col)[numeric_col].sum().reset_index()
                fig2 = px.bar(grouped, x=category_col, y=numeric_col, color=category_col, title=f"{numeric_col} Breakdown")
                st.plotly_chart(fig2, use_container_width=True)

        # Summary stats
        st.markdown("### 📌 Summary Statistics")
        st.write(df[numeric_col].describe())

    except Exception as e:
        st.error("❌ Could not process your file.")
        st.code(str(e))

else:
    st.info("⬆️ Upload a CSV file using the sidebar to begin.")
