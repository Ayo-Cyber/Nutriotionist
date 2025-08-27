import streamlit as st
import pandas as pd
import numpy as np

# --- Page Configuration ---
st.set_page_config(
    page_title="Nutrition Advisor",
    page_icon="🍎",
    layout="wide"
)

# --- Constants ---
EATING_HABIT_RANKING = {'NEVER': 0, 'RARELY': 1, 'OFTEN': 2, 'DAILY': 3}
ACTIVITY_RANKING = {'LIGHT ACTIVE': 0, 'MODERATELY ACTIVE': 1, 'ACTIVE': 2, 'VERY ACTIVE': 3}

# --- Data Loading and Processing ---
@st.cache_data
def load_and_preprocess_data():
    """
    Loads the dataset from a CSV file, preprocesses it by handling missing values,
    and creates ranking columns for categorical features.

    Returns:
        pandas.DataFrame: The preprocessed dataset.
    """
    try:
        df = pd.read_csv('Complete Secondary Data - Sheet1 (1).csv')
        
        # Preprocessing steps
        for col in ['Age', 'Number of meals per day', 'Height in cm', 'Weight', 'BMI']:
            if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                df[col].fillna(df[col].median(), inplace=True)
        
        for col in df.columns:
            if pd.api.types.is_string_dtype(df[col]):
                df[col] = df[col].str.strip().str.upper()
        
        consumption_cols = [col for col in df.columns if 'Consumption Rate' in col]
        for col in consumption_cols:
            df[col + '_Rank'] = df[col].map(EATING_HABIT_RANKING).fillna(0)
            
        if 'Physical Activity level' in df.columns:
            df['Activity_Rank'] = df['Physical Activity level'].map(ACTIVITY_RANKING).fillna(0)
            
        return df
    except FileNotFoundError:
        return None

def categorize_bmi(bmi):
    """Categorizes BMI into different weight statuses."""
    if bmi < 18.5: return 'UNDERWEIGHT'
    if 18.5 <= bmi < 25: return 'NORMAL'
    if 25 <= bmi < 30: return 'OVERWEIGHT'
    if 30 <= bmi < 35: return 'OBESITY (CLASS 1)'
    if 35 <= bmi < 40: return 'OBESITY (CLASS 2)'
    return 'SEVERE/MORBID OBESITY'

# --- UI Components ---
def get_user_input(df):
    """
    Displays sidebar widgets to get user input.

    Args:
        df (pandas.DataFrame): The dataframe, used to populate selectbox options.

    Returns:
        dict: A dictionary containing all the user inputs.
    """
    st.sidebar.header("Enter Your Details")
    
    user_inputs = {
        "bmi": st.sidebar.number_input("Your Body Mass Index (BMI)", min_value=10.0, max_value=60.0, value=25.0, step=0.1),
        "gender": st.sidebar.selectbox("Gender", options=df['Gender'].unique(), format_func=lambda x: x.title()),
        "activity": st.sidebar.selectbox("Physical Activity Level", options=list(ACTIVITY_RANKING.keys()), format_func=lambda x: x.title()),
    }

    st.sidebar.markdown("---_Eating Habits_---")
    user_inputs.update({
        "rice": st.sidebar.selectbox("Rice Consumption", options=list(EATING_HABIT_RANKING.keys()), index=2, format_func=lambda x: x.title()),
        "beans": st.sidebar.selectbox("Beans Consumption", options=list(EATING_HABIT_RANKING.keys()), index=1, format_func=lambda x: x.title()),
        "soft_drinks": st.sidebar.selectbox("Soft Drinks Consumption", options=list(EATING_HABIT_RANKING.keys()), index=1, format_func=lambda x: x.title()),
        "snacks": st.sidebar.selectbox("Snacks Consumption", options=list(EATING_HABIT_RANKING.keys()), index=1, format_func=lambda x: x.title()),
        "fruits": st.sidebar.selectbox("Fruits Consumption", options=list(EATING_HABIT_RANKING.keys()), index=2, format_func=lambda x: x.title()),
        "veg": st.sidebar.selectbox("Vegetables Consumption", options=list(EATING_HABIT_RANKING.keys()), index=2, format_func=lambda x: x.title()),
    })
    
    return user_inputs

def find_best_match(df, user_inputs):
    """
    Finds the best match in the dataset based on user inputs.

    Args:
        df (pandas.DataFrame): The dataset to search.
        user_inputs (dict): The user's input data.

    Returns:
        pandas.Series: The row from the dataframe that is the best match.
    """
    user_bmi_category = categorize_bmi(user_inputs["bmi"])
    user_activity_rank = ACTIVITY_RANKING.get(user_inputs["activity"], 0)

    candidates = df[(df['Gender'] == user_inputs["gender"]) & (df['BMI Category'] == user_bmi_category)].copy()

    if candidates.empty:
        return None

    scores = []
    for _, row in candidates.iterrows():
        score = abs(row['Activity_Rank'] - user_activity_rank) * 2
        score += abs(row['Rice Consumption Rate_Rank'] - EATING_HABIT_RANKING.get(user_inputs["rice"], 0))
        score += abs(row['Beans Consumption Rate_Rank'] - EATING_HABIT_RANKING.get(user_inputs["beans"], 0))
        score += abs(row['Soft drinks Consumption Rate_Rank'] - EATING_HABIT_RANKING.get(user_inputs["soft_drinks"], 0)) * 1.5
        score += abs(row['Snacks Consumption Rate_Rank'] - EATING_HABIT_RANKING.get(user_inputs["snacks"], 0)) * 1.5
        score += abs(row['Fruits Consumption Rate_Rank'] - EATING_HABIT_RANKING.get(user_inputs["fruits"], 0))
        score += abs(row['Vegetables Consumption Rate_Rank'] - EATING_HABIT_RANKING.get(user_inputs["veg"], 0))
        scores.append(score)

    if not scores:
        return None
        
    best_match_index = np.argmin(scores)
    return candidates.iloc[best_match_index]

def display_results(best_match):
    """
    Displays the personalized advice and matched profile details.

    Args:
        best_match (pandas.Series): The best matched row.
    """
    st.subheader("Here is Your Personalized Advice")
    
    if best_match is None:
        st.error("Sorry, we couldn't find a suitable match in our dataset. Please try adjusting your inputs.")
        return

    advice = best_match.get('Dietary advice given', 'No specific advice available.')
    risk = best_match.get('Malnutrition Risk Level', 'Not determined.')

    if risk == 'HIGH RISK':
        st.error(f"**Malnutrition Risk:** {risk.title()}")
    elif risk == 'MEDIUM RISK':
        st.warning(f"**Malnutrition Risk:** {risk.title()}")
    else:
        st.success(f"**Malnutrition Risk:** {risk.title()}")

    st.info(f"**Dietary Advice:** {advice}")

    with st.expander("See Matched Profile Details"):
        st.write(f"**Gender**: {best_match.get('Gender')}")
        st.write(f"**BMI Category**: {best_match.get('BMI Category')}")
        st.write(f"**Activity Level**: {best_match.get('Physical Activity level')}")
        st.write(f"**Dietary Advice**: {best_match.get('Dietary advice given', 'No specific advice available.')}")
        st.write(f"**Malnutrition Risk**: {best_match.get('Malnutrition Risk Level', 'Not determined.')}")

def add_footer():
    """Adds a footer to the page."""
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Made by Wabara Adanma</p>", unsafe_allow_html=True)

# --- Main Application ---
def main():
    """
    The main function that runs the Streamlit application.
    """
    st.title("🍎 Personalized Nutrition Advisor")
    st.markdown("Enter your details in the sidebar to get personalized dietary advice based on our dataset.")

    df = load_and_preprocess_data()

    if df is None:
        st.error("Dataset file not found. Please make sure 'Complete Secondary Data - Sheet1 (1).csv' is in the same directory.")
        return

    user_inputs = get_user_input(df)

    if st.sidebar.button("Get My Advice", use_container_width=True):
        best_match = find_best_match(df, user_inputs)
        display_results(best_match)

    add_footer()

if __name__ == "__main__":
    main()