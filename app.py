import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

# =========================
# LOAD MODEL
# =========================
model = joblib.load("solar_model.pkl")

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Solar Predictor", layout="wide")

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.title("📘 About")
    st.write(
        """
        This app predicts solar energy production using a Machine Learning model (XGBoost).

        ⚡ Built with:
        - Python
        - Streamlit
        - Machine Learning
        """
    )

# =========================
# MAIN TITLE
# =========================
st.title("⚡ Smart Solar Output Prediction System")

st.write("Enter system details to predict annual energy production")

# =========================
# INPUTS
# =========================
col1, col2 = st.columns(2)

with col1:
    pv_size = st.number_input(
        "PV System Size (kWac)", min_value=1, max_value=100000, value=5000
    )
    dc_size = st.number_input(
        "Estimated PV System Size (kWdc)", min_value=1, max_value=100000, value=5500
    )
    storage = st.number_input(
        "Storage Size (kWac)", min_value=0, max_value=50000, value=0
    )

with col2:
    year = st.number_input(
        "Interconnection Year", min_value=2000, max_value=2026, value=2020
    )

    developer = st.selectbox(
        "Developer",
        ["Unknown", "SolarCity", "Sunrun Inc", "Vivint Solar", "Momentum Solar"],
    )

    zip_code = st.text_input("Zip Code", "10001")

# =========================
# FEATURE ENGINEERING
# =========================
dc_ac_ratio = dc_size / (pv_size + 1e-6)
storage_ratio = storage / (pv_size + 1e-6)
system_age = 2026 - year

# =========================
# PREDICTION BUTTON
# =========================
if st.button("Predict", key="predict_btn"):

    # Create input dataframe (ALL REQUIRED FEATURES)
    input_df = pd.DataFrame({
        'PV System Size (kWac)': [pv_size],
        'Estimated PV System Size (kWdc)': [dc_size],
        'Energy Storage System Size (kWac)': [storage],
        'Interconnection Year': [year],
        'Developer': [developer],
        'Zip': [zip_code],

        # Missing categorical fields
        'Utility': ['Unknown'],
        'City/Town': ['Unknown'],
        'County': ['Unknown'],
        'Division': ['Unknown'],
        'Substation': ['Unknown'],
        'Metering Method': ['Unknown'],
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

    # =========================
    # PREDICT
    # =========================
    pred_log = model.predict(input_df)
    prediction = np.expm1(pred_log)[0]

    # =========================
    # OUTPUT
    # =========================
    st.success(f"⚡ Predicted Annual Energy Production: {int(prediction):,} kWh")

    # Monthly estimation
    monthly = prediction / 12
    st.info(f"📅 Estimated Monthly Production: {int(monthly):,} kWh")

    # =========================
    # WARNING LOGIC
    # =========================
    if prediction < pv_size * 800:
        st.warning("⚠️ Low energy production detected. System may be inefficient.")
    else:
        st.success("✅ System performance looks good!")

    # =========================
    # CHART (MONTHLY BREAKDOWN)
    # =========================
    months = [
        "Jan","Feb","Mar","Apr","May","Jun",
        "Jul","Aug","Sep","Oct","Nov","Dec"
    ]
    values = [monthly]*12

    fig, ax = plt.subplots()
    ax.bar(months, values)
    ax.set_title("Estimated Monthly Energy Production (kWh)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Energy (kWh)")

    st.pyplot(fig)

    # =========================
    # ADDITIONAL INFO
    # =========================
    st.markdown("### 📊 Model Info")
    st.write(
        """
        - Model: XGBoost Regressor  
        - Target: Annual PV Energy Production (kWh)  
        - Features: System size, storage, developer, location, engineered ratios  
        """
    )
