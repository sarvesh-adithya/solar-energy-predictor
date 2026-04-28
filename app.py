import streamlit as st
import pandas as pd
import numpy as np
import joblib

# -------------------------------
# Load model
# -------------------------------
model = joblib.load("solar_model.pkl")

st.set_page_config(page_title="Solar AI Predictor", layout="wide")

# -------------------------------
# HEADER
# -------------------------------
st.title("⚡ Smart Solar Output Prediction System")
st.caption("AI-powered solar energy prediction with insights & analytics")

# -------------------------------
# INPUT SECTION
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    pv_size = st.number_input("PV System Size (kWac)", 1.0, 20.0, 5.0)
    dc_size = st.number_input("Estimated PV Size (kWdc)", 1.0, 25.0, 6.0)
    storage = st.number_input("Storage Size (kWac)", 0.0, 20.0, 0.0)

with col2:
    year = st.number_input("Interconnection Year", 2000, 2026, 2020)
    developer = st.selectbox(
        "Developer",
        [
            "Kamtech Solar","SUNCO","Trinity Solar","Momentum Solar",
            "NYS Essential","Patriot Energy","Sunrun Inc",
            "Vivint Solar","SolarCity","Unknown"
        ]
    )
    zip_code = st.text_input("Zip Code", "11418")

# -------------------------------
# PREDICTION
# -------------------------------
if st.button("🚀 Predict Energy Output"):

    try:
        # Feature Engineering
        dc_ac_ratio = dc_size / (pv_size + 1e-6)
        storage_ratio = storage / (pv_size + 1e-6)
        system_age = 2026 - year

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
            'Metering Method': ['NM'],
            'Number of Projects': [1],

            'dc_ac_ratio': [dc_ac_ratio],
            'storage_ratio': [storage_ratio],
            'system_age': [system_age],
            'location_cluster': [0],
            'size_x_age': [pv_size * system_age],
            'size_x_storage': [pv_size * storage],
            'developer_performance': [0]
        })

        pred_log = model.predict(input_df)
        prediction = np.expm1(pred_log)[0]
        monthly = prediction / 12

        # -------------------------------
        # KPI DASHBOARD
        # -------------------------------
        c1, c2, c3 = st.columns(3)
        c1.metric("⚡ Annual Output", f"{int(prediction):,} kWh")
        c2.metric("📅 Monthly Output", f"{int(monthly):,} kWh")
        c3.metric("🔋 System Size", f"{pv_size} kW")

        # -------------------------------
        # CO2 SAVINGS
        # -------------------------------
        co2_saved = prediction * 0.7 / 1000  # tons/year
        st.success(f"🌱 CO₂ Saved: {co2_saved:.2f} tons/year")

        # -------------------------------
        # COST SAVINGS
        # -------------------------------
        savings = prediction * 0.12  # assume ₹ per kWh
        st.info(f"💰 Estimated Yearly Savings: ₹{int(savings):,}")

        # -------------------------------
        # EFFICIENCY
        # -------------------------------
        efficiency = prediction / (pv_size * 365)
        st.write(f"⚙️ Efficiency: {efficiency:.2f} kWh/kW/day")

        # -------------------------------
        # INSIGHT
        # -------------------------------
        if prediction < 4000:
            st.warning("⚠️ Low production system")
        elif prediction < 8000:
            st.info("ℹ️ Moderate production system")
        else:
            st.success("🔥 High performance solar system")

        # -------------------------------
        # MONTHLY GRAPH
        # -------------------------------
        monthly_data = pd.DataFrame({
            "Month": [
                "Jan","Feb","Mar","Apr","May","Jun",
                "Jul","Aug","Sep","Oct","Nov","Dec"
            ],
            "kWh": [monthly] * 12
        })

        st.subheader("📈 Monthly Production Trend")
        st.line_chart(monthly_data.set_index("Month"))

    except Exception as e:
        st.error(f"❌ Error: {e}")
