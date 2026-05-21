import streamlit as st
import pandas as pd
import os

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Weather Forecast App",
    page_icon="🌦️",
    layout="wide"
)

st.title("🌦️ Weather Forecasting App")
st.markdown("Simple Streamlit app using hourly weather dataset")

# =====================================================
# LOAD DATA
# =====================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "hourly_weather_data.csv")


@st.cache_data
def load_data(path):
    return pd.read_csv(path)

try:
    df = load_data(DATA_PATH)
    st.success("✅ Dataset loaded successfully")

except Exception as e:
    st.error(f"❌ Failed to load dataset: {e}")
    st.stop()

# =====================================================
# SHOW DATA
# =====================================================
st.subheader("📄 Weather Data Preview")
st.dataframe(df.head(), use_container_width=True)

# =====================================================
# DATA INFO
# =====================================================
st.subheader("📊 Dataset Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])
col3.metric("Missing Values", int(df.isnull().sum().sum()))

# =====================================================
# COLUMN SELECTION
# =====================================================
st.subheader("📈 Visualization")

numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

if len(numeric_cols) == 0:
    st.warning("No numeric columns found for plotting")
    st.stop()

selected_col = st.selectbox("Select column to visualize", numeric_cols)

# =====================================================
# LINE CHART
# =====================================================
st.line_chart(df[selected_col])

# =====================================================
# MULTI CHART COMPARISON
# =====================================================
st.subheader("📊 Multi-Variable View")

selected_cols = st.multiselect(
    "Select multiple columns",
    numeric_cols,
    default=numeric_cols[:min(3, len(numeric_cols))]
)

if selected_cols:
    st.line_chart(df[selected_cols])

# =====================================================
# DOWNLOAD DATA
# =====================================================
csv = df.to_csv(index=False)

st.download_button(
    label="⬇️ Download Dataset",
    data=csv,
    file_name="hourly_weather_data.csv",
    mime="text/csv"
)

# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit")