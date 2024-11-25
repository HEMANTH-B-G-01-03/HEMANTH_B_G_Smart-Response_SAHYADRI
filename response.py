import openai
import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API key from the environment
my_key = os.getenv("MY_KEY")

# Set your OpenAI API key
openai.api_key = my_key

# Function to generate the email response using chat models (gpt-3.5-turbo or gpt-4)
def generate_email_response(client_first_name, client_last_name, client_email, client_country, client_language, 
                            project_type, service_category, project_details, budget, your_name):
    # Constructing the prompt
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
            model="gpt-3.5-turbo",  # Make sure to use the correct model
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
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


# Streamlit Interface
def run():
    st.title('HEMANTHs Smart  Email Response Generator')

    # Collecting input data from user
    your_name = st.text_input("Your Name")  # Separate input for "Your Name"
    client_first_name = st.text_input("Client First Name")
    client_last_name = st.text_input("Client Last Name")
    client_email = st.text_input("Client Email")
    client_country = st.text_input("Client Country")
    client_language = st.text_input("Client Language")
    project_type = st.text_input("Project Type")
    service_category = st.text_input("Service Category")
    project_details = st.text_area("Project Details")
    budget = st.text_input("Budget")

    # Displaying the input information in a structured format
    if st.button("Generate Email Response"):
        if all([your_name, client_first_name, client_last_name, client_email, client_country, client_language, 
                project_type, service_category, project_details, budget]):
            # Displaying the inquiry information in the desired format
            st.subheader("Client Inquiry Information:")
            st.markdown(f"""
            **From Name**: {client_first_name} {client_last_name}  
            **Client First Name**: {client_first_name}  
            **Client Last Name**: {client_last_name}  
            **Client Email**: {client_email}  
            **Client Country**: {client_country}  
            **Client Language**: {client_language}  
            **Project Type**: {project_type}  
            **Service Category**: {service_category}  
            **Client Website**: No  
            **Additional Information (if any)**:  
            *"{project_details}"  
            **Budget**: {budget}  
            """)

            # Generate the email response
            email_response = generate_email_response(
                client_first_name, client_last_name, client_email, client_country, client_language, 
                project_type, service_category, project_details, budget, your_name
            )

            st.subheader("Generated Email Response:")
            st.text_area("Email Response", email_response, height=250)
        else:
            st.warning("Please fill in all the fields.")

# Run the Streamlit app
if __name__ == "__main__":
    run()
