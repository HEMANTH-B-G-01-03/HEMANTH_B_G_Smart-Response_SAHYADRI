import openai
import os
import streamlit as st
import json
import pandas as pd
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API key from the environment
my_key = os.getenv("MY_KEY")

# Setting OpenAI API key
openai.api_key = my_key

# Function to generate the email response using chat models (gpt-3.5-turbo or gpt-4)
def generate_email_response(client_first_name, client_last_name, client_email, client_country, client_language,
                            project_type, service_category, project_details, budget, your_name):
    prompt = f"""
    You are a professional consultant. You have received a project inquiry with the following details:
    - Client First Name: {client_first_name}
    - Client Last Name: {client_last_name}
    - Client Email: {client_email}
    - Client Country: {client_country}
    - Client Language: {client_language}
    - Project Type: {project_type}
    - Service Category: {service_category}
    - Project Details: {project_details}
    - Budget: {budget}

    Please generate a professional and human-like email response to the client confirming the project details, providing a summary, and suggesting next steps. Avoid generic phrases like "I hope this email finds you well." The response should sound natural and personalized. Address the email using {your_name}.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
        )
        email_response = response['choices'][0]['message']['content'].strip()
        return email_response
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Function to store feedback in JSON format
def store_feedback(feedback_data):
    if os.path.exists("feedback.json"):
        with open("feedback.json", "r") as file:
            try:
                existing_data = json.load(file)
                if not isinstance(existing_data, list):
                    existing_data = []
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []
    existing_data.append(feedback_data)
    with open("feedback.json", "w") as file:
        json.dump(existing_data, file, indent=4)

# Function to read and process feedback data
def load_feedback_data():
    if os.path.exists("feedback.json"):
        with open("feedback.json", "r") as file:
            try:
                feedback_data = json.load(file)
                return feedback_data
            except json.JSONDecodeError:
                return []
    return []

# Machine Learning Model for Feedback Prediction
def train_feedback_model(feedback_data):
    # Extract feedback (suggestions and liked/disliked responses)
    feedback_df = pd.DataFrame(feedback_data)
    
    # Drop entries where the suggestion or liked response is missing
    feedback_df.dropna(subset=["suggestion", "liked_response"], inplace=True)
    
    # Vectorize the suggestions (text data)
    vectorizer = CountVectorizer(stop_words="english")
    X = vectorizer.fit_transform(feedback_df["suggestion"])

    # Convert liked_response to binary (Yes -> 1, No -> 0)
    y = feedback_df["liked_response"].apply(lambda x: 1 if x == "Yes" else 0)
    
    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Train a simple Logistic Regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return model, vectorizer, accuracy

# Function to predict if the response is liked or not based on feedback suggestions
def predict_feedback(model, vectorizer, suggestion):
    X_new = vectorizer.transform([suggestion])
    prediction = model.predict(X_new)
    return "Yes" if prediction[0] == 1 else "No"

# Streamlit Interface
def run():
    st.title('HEMANTHs Smart Email Response Generator')

    # Prefilled values
    prefilled_values = {
        "your_name": "Hemanth B G",
        "client_first_name": "Alice",
        "client_last_name": "Fernandes",
        "client_email": "Fernandes@gmail.com",
        "client_country": "USA",
        "client_language": "English",
        "project_type": "Web Application",
        "service_category": "Full Stack ",
        "project_details": "I need a website which shows the available resort in a particular place...",
        "budget": "10000"
    }

    # Collecting input data from the user and setting prefilled values
    your_name = st.text_input("Your Name", value=prefilled_values["your_name"])
    client_first_name = st.text_input("Client First Name", value=prefilled_values["client_first_name"])
    client_last_name = st.text_input("Client Last Name", value=prefilled_values["client_last_name"])
    client_email = st.text_input("Client Email", value=prefilled_values["client_email"])
    client_country = st.text_input("Client Country", value=prefilled_values["client_country"])
    client_language = st.text_input("Client Language", value=prefilled_values["client_language"])
    project_type = st.text_input("Project Type", value=prefilled_values["project_type"])
    service_category = st.text_input("Service Category", value=prefilled_values["service_category"])
    project_details = st.text_area("Project Details", value=prefilled_values["project_details"])
    budget = st.text_input("Budget", value=prefilled_values["budget"])

    # Button to generate the email
    if st.button("Generate Email Response"):
        if all([your_name, client_first_name, client_last_name, client_email, client_country, client_language, 
                project_type, service_category, project_details, budget]):

            # Generate the email response
            email_response = generate_email_response(
                client_first_name, client_last_name, client_email, client_country, client_language, 
                project_type, service_category, project_details, budget, your_name
            )

            # Display the generated email response
            st.subheader("Generated Email Response:")
            st.text_area("Email Response", email_response, height=250, key="email_response_area")

            # Collect feedback for "Did you like the response?"
            liked_response = st.radio("Did you like the email response?", ("Yes", "No"))

            # Collect suggestions for improvement
            suggestion = st.text_area("Please provide your suggestions on how we can improve the response:", height=200)

            feedback_data = {
                "your_name": your_name,
                "client_first_name": client_first_name,
                "client_last_name": client_last_name,
                "client_email": client_email,
                "email_response": email_response,
                "suggestion": suggestion,
                "liked_response": liked_response
            }
            store_feedback(feedback_data)

            st.success("Feedback submitted successfully!")

        else:
            st.warning("Please fill in all the fields.")

    # Load feedback data
    feedback_data = load_feedback_data()

    # Train model if there is enough data
    if len(feedback_data) > 10:
        model, vectorizer, accuracy = train_feedback_model(feedback_data)
        st.write(f"Model Accuracy: {accuracy:.2f}")

        # Predict feedback for new suggestion
        if st.button("Predict Feedback on a New Suggestion"):
            new_suggestion = st.text_area("Enter a suggestion to predict if it's positive or negative:", "")
            if new_suggestion:
                prediction = predict_feedback(model, vectorizer, new_suggestion)
                st.write(f"The model predicts the feedback will be: {prediction}")

# Run the Streamlit app
if __name__ == "__main__":
    run()
