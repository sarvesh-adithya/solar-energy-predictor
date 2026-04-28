import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ------------------------
# Load model
# ------------------------
model = joblib.load("solar_model.pkl")

# ------------------------
# Page config
# ------------------------
st.set_page_config(page_title="Solar Predictor", layout="wide")

st.title("⚡ Smart Solar Output Prediction System")
st.write("Enter system details to predict annual energy production")

# ------------------------
# INPUT SECTION (2 columns)
# ------------------------
col1, col2 = st.columns(2)

with col1:
    pv_size = st.number_input(
        "PV System Size (kWac)",
        min_value=1.0, max_value=20.0, value=5.0
    )

    dc_size = st.number_input(
        "Estimated PV System Size (kWdc)",
        min_value=1.0, max_value=25.0, value=6.0
    )

    storage = st.number_input(
        "Storage Size (kWac)",
        min_value=0.0, max_value=10.0, value=0.0
    )

with col2:
    year = st.number_input(
        "Interconnection Year",
        min_value=2000, max_value=2026, value=2020
    )

    developer = st.selectbox(
        "Developer",
        ["Unknown", "SolarCity", "Sunrun Inc", "Vivint Solar", "Momentum Solar"]
    )

    zip_code = st.text_input("Zip Code", "10001")

# ------------------------
# PREDICT BUTTON
# ------------------------
if st.button("🚀 Predict Energy Output"):

    try:
        # ------------------------
        # Feature Engineering
        # ------------------------
        dc_ac_ratio = dc_size / (pv_size + 1e-6)
        storage_ratio = storage / (pv_size + 1e-6)
        system_age = 2026 - year

        # ------------------------
        # DataFrame (MATCH MODEL)
        # ------------------------
        input_df = pd.DataFrame({
            'PV System Size (kWac)': [pv_size],
            'Estimated PV System Size (kWdc)': [dc_size],
            'Energy Storage System Size (kWac)': [storage],
            'Interconnection Year': [year],
            'Developer': [developer],
            'Zip': [zip_code],

            'Utility': ['Unknown'],
            'City/Town': ['Unknown'],
            'County': ['Unknown'],
            'Division': ['Unknown'],
            'Substation': ['Unknown'],
            'Metering Method': ['Unknown'],
            'Number of Projects': [1],

            'dc_ac_ratio': [dc_ac_ratio],
            'storage_ratio': [storage_ratio],
            'system_age': [system_age],
            'location_cluster': [0],
            'size_x_age': [pv_size * system_age],
            'size_x_storage': [pv_size * storage],
            'developer_performance': [0]
        })

        # ------------------------
        # Prediction
        # ------------------------
        pred_log = model.predict(input_df)
        prediction = np.expm1(pred_log)[0]

        monthly = prediction / 12

        # ------------------------
        # KPI SECTION
        # ------------------------
        st.divider()

        k1, k2, k3 = st.columns(3)

        k1.metric("⚡ Annual Output", f"{int(prediction):,} kWh")
        k2.metric("📅 Monthly Output", f"{int(monthly):,} kWh")
        k3.metric("🔋 System Size", f"{pv_size:.1f} kW")

        # ------------------------
        # ENVIRONMENT + SAVINGS
        # ------------------------
        co2_saved = prediction * 0.0007
        savings = prediction * 0.12

        st.success(f"🌱 CO₂ Saved: {co2_saved:.2f} tons/year")
        st.info(f"💰 Estimated Yearly Savings: ₹{int(savings):,}")

        # ------------------------
        # EFFICIENCY
        # ------------------------
        efficiency = prediction / (pv_size * 365)
        st.write(f"⚙️ Efficiency: {efficiency:.2f} kWh/kW/day")

        # ------------------------
        # PERFORMANCE SCORE
        # ------------------------
        st.subheader("⚡ System Performance Score")

        score = min(100, int((prediction / 8000) * 100))
        st.progress(score)
        st.write(f"Performance Score: {score}/100")

        # ------------------------
        # ROI CALCULATION
        # ------------------------
        investment = pv_size * 50000
        roi_years = investment / savings if savings != 0 else 0

        st.metric("📊 ROI Period", f"{roi_years:.1f} years")

        # ------------------------
        # SYSTEM STATUS
        # ------------------------
        if prediction < 3000:
            st.warning("⚠️ Low energy production system")
        elif prediction < 7000:
            st.info("ℹ️ Moderate production system")
        else:
            st.success("✅ High performance solar system")

        # ------------------------
        # AI RECOMMENDATION
        # ------------------------
        st.subheader("🤖 AI Recommendation")

        if pv_size < 3:
            st.info("👉 Increase system size for better savings")
        elif storage == 0:
            st.warning("👉 Adding battery storage can improve efficiency")
        else:
            st.success("✅ Your system configuration is optimized")

        # ------------------------
        # MONTHLY TREND (FIXED ORDER)
        # ------------------------
        st.subheader("📈 Monthly Production Trend")

        monthly_values = np.random.normal(monthly, monthly * 0.1, 12)

        monthly_data = pd.DataFrame({
            "Month": [
                "Jan","Feb","Mar","Apr","May","Jun",
                "Jul","Aug","Sep","Oct","Nov","Dec"
            ],
            "kWh": monthly_values
        })

        st.line_chart(monthly_data.set_index("Month"))

        # ------------------------
        # DOWNLOAD REPORT
        # ------------------------
        report = f"""
Solar Report

Annual Energy: {int(prediction)} kWh
Monthly Energy: {int(monthly)} kWh
Savings: ₹{int(savings)}
CO2 Saved: {co2_saved:.2f} tons/year
ROI: {roi_years:.1f} years
"""

        st.download_button(
            "📄 Download Report",
            report,
            file_name="solar_report.txt"
        )

    except Exception as e:
        st.error(f"❌ Error: {e}")
