import streamlit as st
import pandas as pd
import numpy as np
import joblib

# -------------------------------
# Load model
# -------------------------------
model = joblib.load("solar_model.pkl")

# -------------------------------
# UI Title
# -------------------------------
st.set_page_config(page_title="Solar Predictor", layout="wide")

st.title("⚡ Smart Solar Output Prediction System")
st.write("Enter system details to predict annual energy production")

# -------------------------------
# INPUT SECTION (2 columns layout)
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    pv_size = st.number_input(
        "PV System Size (kWac)",
        min_value=1.0,
        max_value=20.0,
        value=5.0
    )

    dc_size = st.number_input(
        "Estimated PV System Size (kWdc)",
        min_value=1.0,
        max_value=25.0,
        value=6.0
    )

    storage = st.number_input(
        "Storage Size (kWac)",
        min_value=0.0,
        max_value=20.0,
        value=0.0
    )

with col2:
    year = st.number_input(
        "Interconnection Year",
        min_value=2000,
        max_value=2026,
        value=2020
    )

    developer = st.selectbox(
        "Developer",
        [
            "Kamtech Solar",
            "SUNCO",
            "Trinity Solar",
            "Momentum Solar",
            "NYS Essential",
            "Patriot Energy",
            "Sunrun Inc",
            "Vivint Solar",
            "SolarCity",
            "Unknown"
        ]
    )

    zip_code = st.text_input("Zip Code", "11418")

# -------------------------------
# PREDICT BUTTON (ONLY ONE)
# -------------------------------
if st.button("Predict", key="predict_button"):

    try:
        # -------------------------------
        # Feature Engineering
        # -------------------------------
        dc_ac_ratio = dc_size / (pv_size + 1e-6)
        storage_ratio = storage / (pv_size + 1e-6)
        system_age = 2026 - year

        # -------------------------------
        # Create DataFrame (ALL columns)
        # -------------------------------
        input_df = pd.DataFrame({
            'PV System Size (kWac)': [pv_size],
            'Estimated PV System Size (kWdc)': [dc_size],
            'Energy Storage System Size (kWac)': [storage],
            'Interconnection Year': [year],
            'Developer': [developer],
            'Zip': [zip_code],

            # Default categorical values
            'Utility': ['Unknown'],
            'City/Town': ['Unknown'],
            'County': ['Unknown'],
            'Division': ['Unknown'],
            'Substation': ['Unknown'],
            'Metering Method': ['NM'],
            'Number of Projects': [1],

            # Engineered features
            'dc_ac_ratio': [dc_ac_ratio],
            'storage_ratio': [storage_ratio],
            'system_age': [system_age],
            'location_cluster': [0],
            'size_x_age': [pv_size * system_age],
            'size_x_storage': [pv_size * storage],
            'developer_performance': [0]
        })

        # -------------------------------
        # Prediction
        # -------------------------------
        pred_log = model.predict(input_df)
        prediction = np.expm1(pred_log)[0]

        # -------------------------------
        # Display Results
        # -------------------------------
        st.success(f"⚡ Predicted Annual Energy Production: {int(prediction):,} kWh")

        monthly = prediction / 12
        st.info(f"📅 Estimated Monthly Production: {int(monthly):,} kWh")

        # -------------------------------
        # Simple Insight
        # -------------------------------
        if prediction < 4000:
            st.warning("⚠️ Low energy production system")
        elif prediction < 8000:
            st.info("ℹ️ Moderate energy production")
        else:
            st.success("✅ High performing solar system")

        # -------------------------------
        # Chart
        # -------------------------------
        chart_data = pd.DataFrame({
            "Metric": ["Annual Output"],
            "kWh": [prediction]
        })

        st.bar_chart(chart_data.set_index("Metric"))

    except Exception as e:
        st.error(f"❌ Error: {e}")
