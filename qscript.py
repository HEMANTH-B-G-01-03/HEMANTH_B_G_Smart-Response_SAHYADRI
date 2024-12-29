import openai  # interacting with the OpenAI API
import os  # to interact with the os and to read the env variable
import streamlit as st  # for the web interface
import json  # handling JSON files
from dotenv import load_dotenv  # to read the variables from the .env file

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API key from the environment
my_key = os.getenv("MY_KEY")

# Setting OpenAI API key
openai.api_key = my_key

# Function to generate the email response using chat models (gpt-3.5-turbo or gpt-4)
def generate_email_response(client_first_name, client_last_name, client_email, client_country, client_website,client_language, project_type, service_category, project_details, budget, your_name):
    # This prompt is going to explain to the AI what kind of response to generate, including tone and content.
    prompt = f"""
    You are a professional consultant. You have received a project inquiry with the following details:

    - Client First Name: {client_first_name}
    - Client Last Name: {client_last_name}
    - Client Email: {client_email}
    - Client Country: {client_country}
    - Client Website: {client_website}
    - Client Language: {client_language}
    - Project Type: {project_type}
    - Service Category: {service_category}
    - Project Details: {project_details}
    - Budget: {budget}

    Please generate a professional and human-like email response in {client_language}. Confirm the project details, provide a summary, and suggest next steps. Avoid generic phrases like "I hope this email finds you well." The response should sound natural and personalized. Address the email using {your_name}. Also mention about the website  preferd also {client_website} , in the response make sure to  mention the phrase best regards from {your_name} at the end of all the responses  , write the subject also for all the responses 
    """

    # Try to make the API call to OpenAI
    try:
        # Using openai.ChatCompletion.create() for chat models like gpt-3.5-turbo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,  # this is the maximum number of words of email to be generated
            temperature=0.3  # lower the value of this it will give more precise and accurate response in the email
        )

        # Extracting the email response text
        email_response = response['choices'][0]['message']['content'].strip()

        return email_response

    except openai.error.InvalidRequestError as e:
        return f"Invalid Request Error: {str(e)}"
    except openai.error.AuthenticationError as e:
        return f"Authentication Error: Please check your API key. {str(e)}"
    except openai.error.RateLimitError as e:
        return f"Rate Limit Error: You have hit the rate limit. {str(e)}"
    except Exception as e:
        return f"Error generating response: {str(e)}"


# Function to collect feedback from users and store it in a file (JSON)
def collect_feedback(your_name, client_first_name, client_last_name, client_email, email_response):
    st.markdown("### If you didn’t like the response, please fill in the feedback below.")

    # Display a suggestion text area for feedback
    suggestion = st.text_area("Please provide your suggestions on how we can improve the response:", height=200)

    # Button to submit the feedback
    submit_button = st.button("Submit Feedback")

    # If the submit button is clicked, store the feedback
    if submit_button:
        feedback_data = {
            "your_name": your_name,
            "client_first_name": client_first_name,
            "client_last_name": client_last_name,
            "client_email": client_email,
            "email_response": email_response,
            "suggestion": suggestion  # Saving the suggestion (can be empty if no suggestion is provided)
        }
        store_feedback(feedback_data)
        st.success("Feedback submitted successfully!")  # Displaying success message

    return suggestion

# Function to store feedback in JSON format
def store_feedback(feedback_data):
    # Check if the feedback.json file exists
    if os.path.exists("feedback.json"):
        # If the file exists, open and read its content
        with open("feedback.json", "r") as file:
            try:
                existing_data = json.load(file)
                # Ensure that existing_data is a list (in case it's empty, initialize it as an empty list)
                if not isinstance(existing_data, list):
                    existing_data = []
            except json.JSONDecodeError:
                # If the JSON file is empty or malformed, reset it to an empty list
                existing_data = []
    else:
        # If the file doesn't exist, initialize it as an empty list
        existing_data = []

    # Append the new feedback data to the list
    existing_data.append(feedback_data)

    # Save the updated list back to the feedback.json file
    with open("feedback.json", "w") as file:
        json.dump(existing_data, file, indent=4)


# Function to collect the 'Yes' or 'No' feedback separately
def collect_liked_feedback():
    liked_response = st.selectbox("did you  like the response",["yes","no"])
    
    return liked_response
# Streamlit Interface
def run():
    st.title('Hemanth\'s Smart Email Response Generator')
    # Prefilled values
    prefilled_values = {
        "your_name": "Hemanth B G",
        "client_first_name": "Alice",
        "client_last_name": "Fernandes",
        "client_website": "www.google.com",
        "client_email": "Fernandes@gmail.com",
        "client_country": "USA",
        "client_language": "English",
        "project_type": "Web Application",
        "service_category": "Full Stack",
        "project_details": "I need a website which shows the available resorts in a particular place, it must show all the available resorts in that place and apply filtering to amount, based on the star rating. I need the dates to be booked from and till which date, then the total amount has to be calculated and after booking the invoice must be obtained in the pdf format.",
        "budget": "10000"
    }

    # Collecting input data from the user and setting prefilled values
    your_name = st.text_input("Your Name", value=prefilled_values["your_name"])
    client_first_name = st.text_input("Client First Name", value=prefilled_values["client_first_name"])
    client_last_name = st.text_input("Client Last Name", value=prefilled_values["client_last_name"])
    client_email = st.text_input("Client Email", value=prefilled_values["client_email"])
    client_website=st.text_input("Enter the prefered client website", prefilled_values["client_website"])
    client_country = st.text_input("Client Country", value=prefilled_values["client_country"])
    client_language = st.selectbox("Client Language", ["English", "Spanish", "French", "German", "Italian", "Portuguese"])
    project_type = st.text_input("Project Type", value=prefilled_values["project_type"])
    service_category = st.text_input("Service Category", value=prefilled_values["service_category"])
    project_details = st.text_area("Project Details", value=prefilled_values["project_details"])
    budget = st.text_input("Budget", value=prefilled_values["budget"])
    # Button to generate the email
    if st.button("Generate Email Response"):
        if all([your_name, client_first_name, client_last_name, client_email, client_country, client_website ,client_language,
                project_type, service_category, project_details, budget]):
            # Generate the email response
            email_response = generate_email_response(
                client_first_name, client_last_name, client_email, client_country, client_website,client_language,
                project_type, service_category, project_details, budget, your_name
            )
            # Display the generated email response
            st.subheader("Generated Email Response:")
            st.text_area("Email Response", email_response, height=250, key="email_response_area")

            # Collect feedback for "Did you like the response?"
            liked_response = collect_liked_feedback()

            # Collect suggestions for improvement
            collect_feedback(your_name, client_first_name, client_last_name, client_email, email_response)
            feed1=" it was good"
            # Store the liked/disliked feedback separately
            feedback_data = {

                "your_name": your_name,
                "client_first_name": client_first_name,
                "client_last_name": client_last_name,
                "client_email": client_email,
                "liked_response": liked_response,  # Storing whether they liked the response
                "feedback":feed1

            }
            store_feedback(feedback_data)

        else:
            st.warning("Please fill in all the fields.")

# Run the Streamlit app
if __name__ == "__main__":
    run()
