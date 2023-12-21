import streamlit as st
import streamlit.components.v1 as stc
import pickle
import os

# Get the directory of the current script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the file
file_path = os.path.join(script_directory, 'Random_Forest_model.pkl')

# Check if the file exists before attempting to open it
if os.path.exists(file_path):
    # Open the file using the full path
    with open(file_path, 'rb') as file:
        Random_Forest_Model = pickle.load(file)
else:
    st.error(f"Model file not found at {file_path}")
    st.stop()

# Page settings
st.set_page_config(
    page_title="Loan Eligibility Prediction App",
    page_icon="🗝️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': "This app provides predictions for loan eligibility based on user input."}
)

# Set up main page
col1, col2 = st.columns((6, 1))
col1.title("🦉 LOAN ELIGIBILITY PREDICTION ASSISTANT 🦉")
col2.image("assets/Streamlit Loan Pred Logo (3).png")
st.sidebar.image("assets/Streamlit Loan Pred Logo (1).png")
action = st.sidebar.radio("What would you like to do?", ("Run Loan Eligibility Prediction 📊",))

st.markdown("Welcome to our Loan Prediction App!")
st.markdown("This cutting-edge tool empowers our insurance team to accurately predict loan eligibility. Discover the future of finance at your fingertips!")
st.markdown("Unleash the power of algorithms to make data-driven decisions. 🤖💡")

def main():
    run_ml_app()

def run_ml_app():
    # Use st.columns to create two side-by-side columns
    left, right = st.columns(2)

    # User inputs with improved styling
    gender = left.selectbox('Gender', ('Male', 'Female'))
    married = right.selectbox('Married', ('Yes', 'No'))
    dependent = left.selectbox('Dependents', ('None', 'One', 'Two', 'Three'))
    education = right.selectbox('Education', ('Graduate', 'Non-Graduate'))
    self_employed = left.selectbox('Self-Employed', ('Yes', 'No'))
    applicant_income = right.number_input('Applicant Income', value=0, step=100, format='%d')
    coApplicant_income = left.number_input('Co-Applicant Income', value=0, step=100, format='%d')
    loan_amount = right.number_input('Loan Amount', value=0, step=100, format='%d')
    loan_amount_term = left.number_input('Loan Tenor (In Months)', value=0, step=12, format='%d')
    credit_history = right.number_input('Credit History', 0.0, 1.0, value=0.0, step=0.1)
    property_area = st.selectbox('Property Area', ('Semiurban', 'Urban', 'Rural'))

    # Predict button with enhanced styling
    button = st.button('Predict', key='predict_button', help='Click to predict loan eligibility')

    # If the Predict button is clicked
    if button:
        # Make prediction
        result = predict(gender, married, dependent, education, self_employed, applicant_income, coApplicant_income,
                         loan_amount, loan_amount_term, credit_history, property_area)

        # Display result with improved styling
        if result == 'Eligible':
            st.success(f'🎉 Congratulations! You are {result} for the loan.')
        else:
            st.warning(f'⚠️ Sorry, you are {result} for the loan. Please review your inputs.')

def predict(gender, married, dependent, education, self_employed, applicant_income, coApplicant_income,
            loan_amount, loan_amount_term, credit_history, property_area):
    # processing user input
    gen = 0 if gender == 'Male' else 1
    mar = 0 if married == 'Yes' else 1
    dep = float(0 if dependent == 'None' else 1 if dependent == 'One' else 2 if dependent == 'Two' else 3)
    edu = 0 if education == 'Graduate' else 1
    sem = 0 if self_employed == 'Yes' else 1
    pro = 0 if property_area == 'Semiurban' else 1 if property_area == 'Urban' else 2
    lam = loan_amount / 1000
    cap = coApplicant_income / 1000

    # Making prediction
    prediction = Random_Forest_Model.predict(
        [[gen, mar, dep, edu, sem, applicant_income, cap, lam, loan_amount_term, credit_history, pro]])
    result = 'Not Eligible' if prediction == 0 else 'Eligible'

    return result

if __name__ == "__main__":
    main()
