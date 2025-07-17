import streamlit as st
import pandas as pd
import joblib

st.markdown("""
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1504384308090-c894fdcc538d") no-repeat center center fixed;
        background-size: cover;
    }
    .overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        backdrop-filter: blur(2px);
        background-color: rgba(0, 0, 0, 0.6);
        z-index: 0;
    }
    .main > div {
        position: relative;
        z-index: 1;
    }
    h1, label, .stTextInput label, .stSelectbox label, .stNumberInput label {
        color: white !important;
    }
    </style>
    <div class="overlay"></div>
""", unsafe_allow_html=True)


#Load model
model = joblib.load('salary_model.pkl')

st.title("💼Employee Salary Prediction💰")

#initialize session state for inputs
default_state = {
    "age": None,
    "exp": None,
    "edu": 'Select...',
    "job": 'Select...',
    "loc": 'Select...'
}
for key, default in default_state.items():
    if key not in st.session_state:
        st.session_state[key] = default

#Form
with st.form("salary_form"):
    age = st.number_input("Age", min_value=18, max_value=65, value=st.session_state.age, key="age", placeholder="Enter your Age")
    experience = st.number_input("Years of Experience", min_value=0, max_value=50, value=st.session_state.exp, key="exp", placeholder="Enter Experience")
    education = st.selectbox("Education Level", ['Select...', 'High School', "Bachelor's", "Master's", 'PhD'], index=['Select...', 'High School', "Bachelor's", "Master's", 'PhD'].index(st.session_state.edu), key="edu")
    job = st.selectbox("Job Title", ['Select...', 'Business Analyst','Software Engineer','HR Manager','ML Engineer','Data Engineer','Data Scientist','Research Scientist','Project Manager','Marketing Manager','Frontend Devloper'], index=['Select...', 'Business Analyst','Software Engineer','HR Manager','ML Engineer','Data Engineer','Data Scientist','Research Scientist','Project Manager','Marketing Manager','Frontend Devloper'].index(st.session_state.job), key="job")
    location = st.selectbox("Location", ['Select...', 'Mumbai','Austin','Chennai','Atlanta','Banglore','Denver','Seattle','Hyderabad','Kolkata','Boston'], index=['Select...', 'Mumbai','Austin','Chennai','Atlanta','Banglore','Denver','Seattle','Hyderabad','Kolkata','Boston'].index(st.session_state.loc), key="loc")

    col1, col2 = st.columns(2)
    with col1:
        predict = st.form_submit_button("Predict Salary")
   

#Prediction logic
if predict:
    if st.session_state.age is None or st.session_state.exp is None or st.session_state.edu == 'Select...' or st.session_state.job == 'Select...' or st.session_state.loc == 'Select...':
        st.warning("Please fill in all fields before predicting.")
    else:
        input_data = pd.DataFrame([{
            'Age': st.session_state.age,
            'Years_Experience': st.session_state.exp,
            'Education_Level': st.session_state.edu,
            'Job_Title': st.session_state.job.lower().strip(),
            'Location': st.session_state.loc
        }])
        try:
            prediction = model.predict(input_data)[0]
            st.markdown(f"""<h3 style='color:white; text-align: center; padding-top: 20px; font-weight: bold;'>Predicted Salary: Rs {int(prediction):,}</h3>""", unsafe_allow_html=True)

        except Exception as e:
            st.error(f" Error: {e}")

