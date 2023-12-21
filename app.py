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
st.title("Loan Eligibility Prediction Assistant 🦉🌲")
st.sidebar.image("assets/Streamlit Loan Pred Logo (1).png")

# Key Features
st.sidebar.write("Key Features:")
st.sidebar.write("1. **User-Friendly Interface:** Our streamlined interface ensures a seamless experience, making it easy for you to input your details and receive predictions effortlessly.")
st.sidebar.write("2. **Advanced Predictive Modeling:** The app utilizes a Random Forest machine learning model trained on historical data to provide accurate and reliable predictions for loan eligibility.")
st.sidebar.write("3. **Intuitive Inputs:** Input your information with ease using the user-friendly form, including details like gender, marital status, education, income, and more.")
st.sidebar.write("4. **Instant Results:** Receive instant predictions with just a click of a button. The app analyzes your input and provides clear insights into your eligibility for a loan.")
st.sidebar.write("5. **Interactive Visualization:** Visualize the impact of different factors on your eligibility through a clean and interactive display, helping you understand how each variable influences the prediction.")

# How to Use
st.sidebar.write("\nHow to Use:")
st.sidebar.write("1. **Fill in Your Details:** Provide essential information such as gender, marital status, education, and financial details through the intuitive form.")
st.sidebar.write("2. **Click Predict:** Hit the 'Predict' button to let the app process your inputs through the advanced machine learning model.")
st.sidebar.write("3. **Receive Instant Feedback:** Get immediate feedback on your loan eligibility. Celebrate your eligibility with a 🎉 or receive guidance for improvement with a ⚠️.")

st.sidebar.write("\nWhether you're planning your financial future or seeking guidance for loan approval, our Loan Eligibility Prediction Assistant is here to assist you. Empower yourself with data-driven decisions and explore the possibilities of your financial journey! 🚀")

# Apply styling to all texts
text_style = """
    font-family: "Source Code Pro", monospace, 'Courier New', Courier, monospace;
    font-weight: 600;
    color: rgb(0, 0, 0);
    letter-spacing: -0.005em;
    padding: 0.5rem 0px 1rem;
    margin: 0px;
    line-height: 1.2;
"""

st.markdown(f'<style>{text_style}</style>', unsafe_allow_html=True)

st.markdown("Welcome to our Loan Prediction App!")
st.markdown("This cutting-edge tool empowers our insurance team to accurately predict loan eligibility. Discover the future of finance at your fingertips!")
st.markdown("Unleash the power of algorithms to make data-driven decisions. 🤖💡")

def main():
    run_ml_app()

st.subheader("Run Loan Approval Prediction! 🗝️")

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
