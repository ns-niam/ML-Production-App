import streamlit as st
import requests
import pandas as pd

API_URL = "https://stunning-giggle-4jvg7jj9p9r4cqr9q-8000.app.github.dev/predict"

# Page config
st.set_page_config(page_title="ML Prediction App", page_icon="🚀", layout="centered")

# Class mapping
CLASS_NAMES = {
    0: "🌸 Setosa",
    1: "🌼 Versicolor",
    2: "🌺 Virginica"
}

# Sidebar
st.sidebar.title("⚙️ Controls")
if st.sidebar.button("Use Setosa Sample"):
    st.session_state.features = [5.1, 3.5, 1.4, 0.2]
if st.sidebar.button("Use Versicolor Sample"):
    st.session_state.features = [6.0, 2.9, 4.5, 1.5]
if st.sidebar.button("Use Virginica Sample"):
    st.session_state.features = [6.5, 3.0, 5.5, 2.0]

if st.sidebar.button("Clear History"):
    st.session_state.history = []

# Init session state
if "features" not in st.session_state:
    st.session_state.features = [5.1, 3.5, 1.4, 0.2]

if "history" not in st.session_state:
    st.session_state.history = []

# Title
st.markdown("<h1 style='text-align: center;'>🚀 ML Prediction App</h1>", unsafe_allow_html=True)
st.markdown("---")

# Input UI
col1, col2 = st.columns(2)

with col1:
    f1 = st.number_input("Feature 1", value=st.session_state.features[0])
    f2 = st.number_input("Feature 2", value=st.session_state.features[1])

with col2:
    f3 = st.number_input("Feature 3", value=st.session_state.features[2])
    f4 = st.number_input("Feature 4", value=st.session_state.features[3])

# Predict button
if st.button("🔮 Predict", use_container_width=True):
    data = {"data": [f1, f2, f3, f4]}

    with st.spinner("Predicting..."):
        try:
            response = requests.post(API_URL, json=data, timeout=10)

            if response.status_code == 200:
                result = response.json()

                pred = result["prediction"][0]
                conf = result["confidence"][0]

                st.success(f"Prediction: {CLASS_NAMES.get(pred, pred)}")

                # Confidence chart
                df = pd.DataFrame({
                    "Class": ["Setosa", "Versicolor", "Virginica"],
                    "Confidence": conf
                })

                st.subheader("📊 Confidence")
                st.bar_chart(df.set_index("Class"))

                # Save history
                st.session_state.history.append({
                    "Input": [f1, f2, f3, f4],
                    "Prediction": CLASS_NAMES.get(pred, pred)
                })

            else:
                st.error(f"API Error: {response.text}")

        except Exception as e:
            st.error(f"Connection Error: {e}")

# History section
if st.session_state.history:
    st.markdown("---")
    st.subheader("📜 Prediction History")

    history_df = pd.DataFrame(st.session_state.history)
    st.dataframe(history_df, use_container_width=True)