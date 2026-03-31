import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Delhi Air Quality Analysis", layout="wide")

# App Title
st.title("🌫 Delhi Air Quality Analysis in Delhi")

# File Upload
uploaded_file = st.file_uploader("Upload your Delhi Air Quality Dataset (.csv)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Convert Date column if available
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])

    # Display Data
    st.subheader("📌 Dataset Preview")
    st.dataframe(df.head())

    # Summary Statistics
    st.subheader("📊 Summary Statistics")
    st.write(df.describe())

    # Missing Values
    ms = df.isnull().sum()
    st.subheader("⚠ Missing Values Check")
    st.write(ms)

    # AQI Classification Function
    def classify_aqi(aqi):
        if aqi <= 50: return "Good"
        elif aqi <= 100: return "Satisfactory"
        elif aqi <= 200: return "Moderate"
        elif aqi <= 300: return "Poor"
        elif aqi <= 400: return "Very Poor"
        else: return "Severe"

    # Apply AQI Class if AQI exists
    if "AQI" in df.columns:
        df["AQI Category"] = df["AQI"].apply(classify_aqi)

        st.subheader("🏷 AQI Category Count")
        st.bar_chart(df["AQI Category"].value_counts())

    # AQI Trend Chart
    if "Date" in df.columns and "AQI" in df.columns:
        st.subheader("📈 AQI Trend Over Time")
        st.line_chart(df.set_index("Date")["AQI"])

    # Major Pollutants Trend
    st.subheader("🧪 Pollutants Trend Analysis")
    pollutants = [p for p in ["PM2.5", "PM10", "NO2"] if p in df.columns]
    
    if pollutants:
        st.line_chart(df[pollutants])
    else:
        st.write("No major pollutant columns found in dataset")

    # Worst AQI Day
    if "AQI" in df.columns:
        worst_day = df[df["AQI"] == df["AQI"].max()]
        st.subheader("🔥 Worst AQI Day")
        st.write(worst_day)

else:
    st.info("👆 Upload a CSV file to begin analysis")