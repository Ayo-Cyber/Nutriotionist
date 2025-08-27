# Personalized Nutrition Advisor

This project is a Streamlit web application that provides personalized dietary advice to users based on their health details and eating habits. The application matches user input to a dataset of patient profiles to find the most similar case and offers the dietary recommendations associated with that profile.

## Features

-   **User Input:** Collects user data through a simple sidebar form, including BMI, gender, physical activity level, and consumption frequency of various foods.
-   **Personalized Advice:** Utilizes a matching algorithm to find a similar profile within the dataset and displays the corresponding dietary advice and malnutrition risk level.
-   **Data-Driven:** Powered by a dataset containing anonymous patient information and the dietary advice they received.
-   **Interactive UI:** Built with Streamlit for a clean and user-friendly web interface.

## Dataset

The application uses the `Complete Secondary Data - Sheet1 (1).csv` file, which contains various patient attributes, including:
-   Demographics (Age, Gender)
-   Eating and Snacking Habits
-   Consumption Rates for different food groups
-   Physical Activity Level
-   BMI and BMI Category
-   Malnutrition Risk Level
-   Dietary Advice Given

## Installation

To run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/Nutriotionist.git
    cd Nutriotionist
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Once the installation is complete, you can run the Streamlit application with the following command:

```bash
streamlit run main.py
```

Your web browser should open with the application running. Fill in your details in the sidebar and click "Get My Advice" to receive your personalized recommendation.

## Dependencies

This project relies on the following Python libraries:

-   [Streamlit](https://streamlit.io/)
-   [Pandas](https://pandas.pydata.org/)
-   [NumPy](https://numpy.org/)

## Credits

This application was created by **Wabara Adanma And Atunrase Ayomide**.