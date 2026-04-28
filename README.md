# ⚡ Smart Solar Output Prediction System

A machine learning powered web application that predicts solar energy production and provides actionable insights like ROI, savings, and efficiency.

---

## 🚀 Live App
👉 https://solar-energy-predictor-lby9y3dbm5nvcp6vvhkj3r.streamlit.app

---

## 📌 Features

- 🔋 Predict annual solar energy output
- 📅 Monthly production estimation
- 🌱 CO₂ emission reduction calculation
- 💰 Yearly savings estimation
- 📊 ROI (Return on Investment) analysis
- ⚡ System performance score
- 🤖 AI-based recommendations
- 📈 Monthly production trend visualization
- 📄 Downloadable solar report

---

## 🧠 Tech Stack

- Python
- Streamlit
- Scikit-learn
- XGBoost
- Pandas / NumPy

---

## 📊 Model Details

- Machine Learning Model: XGBoost Regressor
- Input Features:
  - PV System Size
  - DC Size
  - Storage Size
  - Year
  - Developer
  - Location Features

---

## 💡 How it Works

1. User enters system details
2. Model predicts annual energy output
3. App calculates:
   - Monthly production
   - CO₂ savings
   - Financial savings
   - ROI
4. Displays insights and recommendations

---

## 📸 Screenshot
<img width="1904" height="658" alt="Screenshot 2026-04-28 125014" src="https://github.com/user-attachments/assets/5315d540-cd27-48b9-b43a-ced5e6ab6078" />
<img width="1903" height="774" alt="Screenshot 2026-04-28 125038" src="https://github.com/user-attachments/assets/57d2f15f-69c7-4d3e-a319-c0d41a632d8e" />
<img width="1919" height="787" alt="Screenshot 2026-04-28 125050" src="https://github.com/user-attachments/assets/f3221eb8-5b46-4025-a144-4b6661d59c1d" />







---

## 🛠️ Installation

```bash
git clone https://github.com/sarvesh-adithya/solar-energy-predictor.git
cd solar-energy-predictor
pip install -r requirements.txt
streamlit run app.py
