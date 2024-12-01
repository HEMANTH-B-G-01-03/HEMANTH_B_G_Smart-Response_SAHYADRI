import openai    #interacting with the open ai 
import os           # to interact with the os and to read the evn variable 
import streamlit as st    #  for  web interface 
import json             # hadeling json files 

from dotenv import load_dotenv   # to read the  variables  from evn file 

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API key from the environment
my_key = os.getenv("MY_KEY")

# seting my open ai  jey 
openai.api_key = my_key

# Function to generate the email response using chat models (gpt-3.5-turbo or gpt-4)
def generate_email_response(client_first_name, client_last_name, client_email, client_country, client_language, 
                            project_type, service_category, project_details, budget, your_name):
    
    
    # This  prompt is going to exolain  AI what kind of response to generate, including tone and content.
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



    # Try to make the API call to OpenAI
    try:
        # Using openai.ChatCompletion.create() for chat models like gpt-3.5-turbo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,  # this is the maximum number of words of email to be generated  
            temperature=0.7   # lower the value of this it will give more precise and accurate response in the email
        )

        # Extracting the email response text

        email_response = response['choices'][0]['message']['content'].strip()  #  The response is a JSON object containing various details, including the generated email text.

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
    # Storing feedback in JSON format
    if os.path.exists("feedback.json"):
        with open("feedback.json", "r") as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    existing_data.append(feedback_data)
    with open("feedback.json", "w") as file:
        json.dump(existing_data, file, indent=4)

# Function to collect the 'Yes' or 'No' feedback separately
def collect_liked_feedback():
    liked_response = st.radio("Did you like the email response?", ("Yes", "No"))
    return liked_response


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
        "project_details": "I need a website which shows the available resort in a particular place, it must show all the available resort in that place and concept of filtering must be applied to amount, based on the star rating I need the dates to be booked from and till which date, then total amount has to be calculated and after booking the invoice must be obtained in the pdf format.",
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
            liked_response = collect_liked_feedback()

            # Collect suggestions for improvement
            collect_feedback(your_name, client_first_name, client_last_name, client_email, email_response)

            # Store the liked/disliked feedback separately
            feedback_data = {
                "your_name": your_name,
                "client_first_name": client_first_name,
                "client_last_name": client_last_name,
                "client_email": client_email,
                "liked_response": liked_response  # Storing whether they liked the response
            }
            store_feedback(feedback_data)

        else:
            st.warning("Please fill in all the fields.")

# Run the Streamlit app
if __name__ == "__main__":
    run()
