import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Page settings
st.set_page_config(page_title="Solar Predictor", layout="centered")

# Load model
model = joblib.load("solar_model.pkl")

# Title
st.title("☀️ Solar Energy Production Predictor")
st.markdown("### ⚡ Smart Solar Output Prediction System")

st.write("Enter system details to predict annual energy production")

# Sidebar
st.sidebar.title("About")
st.sidebar.info("""
This app predicts solar energy production using a Machine Learning model (XGBoost).

Built with:
- Python
- Streamlit
- Machine Learning
""")

# Inputs
pv_size = st.number_input("PV System Size (kWac)", value=5000)
dc_size = st.number_input("Estimated PV System Size (kWdc)", value=5500)
storage = st.number_input("Storage Size (kWac)", value=0)
year = st.number_input("Interconnection Year", value=2020)

developer = st.text_input("Developer", "Unknown")
zip_code = st.text_input("Zip Code", "10001")

# Predict button
if st.button("Predict"):

    try:
        # Create dataframe with ALL required features
        input_df = pd.DataFrame({
            'PV System Size (kWac)': [pv_size],
            'Estimated PV System Size (kWdc)': [dc_size],
            'Energy Storage System Size (kWac)': [storage],
            'Interconnection Year': [year],
            'Developer': [developer],
            'Zip': [zip_code],

            # Default placeholders
            'Utility': ['Unknown'],
            'City/Town': ['Unknown'],
            'County': ['Unknown'],
            'Division': ['Unknown'],
            'Substation': ['Unknown'],
            'Metering Method': ['Unknown'],
            'Number of Projects': [1],

            # Feature engineering
            'dc_ac_ratio': [dc_size / (pv_size + 1e-6)],
            'storage_ratio': [storage / (pv_size + 1e-6)],
            'system_age': [2026 - year],
            'location_cluster': [0],
            'size_x_age': [pv_size * (2026 - year)],
            'size_x_storage': [pv_size * storage],
            'developer_performance': [0]
        })

        # Prediction
        pred_log = model.predict(input_df)
        prediction = np.expm1(pred_log)[0]

        # Main result
        st.success(f"⚡ Predicted Annual Energy Production: {int(prediction):,} kWh")

        # Metric display
        st.metric(
            label="Estimated Energy (kWh)",
            value=f"{int(prediction):,}"
        )

        # Monthly estimate
        monthly = prediction / 12
        st.info(f"📅 Estimated Monthly Production: {int(monthly):,} kWh")

        # Performance insight
        if prediction > 30000:
            st.success("✅ High energy production system")
        elif prediction > 15000:
            st.info("⚡ Moderate energy production system")
        else:
            st.warning("⚠️ Low energy production system")

        # Better chart
        chart_data = pd.DataFrame({
            "Metric": ["Energy Output"],
            "Value": [prediction]
        })

        st.bar_chart(chart_data.set_index("Metric"))

    except Exception as e:
        st.error(f"❌ Error: {e}")