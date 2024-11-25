# HEMANTH_B_G_SMARTCLIENTRESPONSE_SAHYADRI
## Smart-Response
This project generates professional, human-like email responses based on client details using OpenAI's GPT model. The application uses Streamlit for the user interface and loads the OpenAI API key securely from a `.env` file.

## Getting Started 

These instructions will help you set up the project and run it locally.

### Prerequisites

- **Python 3.7 or higher** is required. You can download it from [python.org](https://www.python.org/downloads/).
- **OpenAI API Key**: You'll need an API key from OpenAI. You can create one at [OpenAI](https://platform.openai.com/account/api-keys).

### Installation Steps

Follow these steps to get the project up and running:

1. **Clone the Repository:**

   Clone the repository to your local machine:

   ```bash
   git clone https://github.com/Balamurali950/HEMANTH_B_G_Smart-Response_SAHYADRI.git
   cd RepositoryName

2. **Create a virtual environment: Run the following command to create a virtual environment:**

    ```bash
     python -m venv venv

3. **Activate the Virtual Environment:**
    on Windows 

    ```bash
     venv\Scripts\activate

     on linux\ MAC

     ```bash
     source venv/bin/activate
4. **Install Dependencies: Install all necessary dependencies using pip:**

    
     pip install -r requirements.txt

5. **Set Up Your OpenAI API Key:**
    Create a .env file in the root directory of the project.
    Inside the .env file, add the following line with your OpenAI API key:

    
     my_key=your_actual_api_key

6. **Make Sure .env is Added to .gitignore:**
    Add .env to .gitignore to prevent it from being pushed to GitHub:

    
        .env

# RUNNING THE APP 

1. **Run the Streamlit App: After completing the setup, run the following command:**
    streamlit run main.py

2. **Open the App: Open your web browser and go to http://localhost:8501 to see the app running.**




