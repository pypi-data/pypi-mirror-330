# Import required libraries
import google.generativeai
import os
from dotenv import load_dotenv

# Define a function to generate a response using the Gemini model
def Gogo(user_prompt):
    """
    Generate a response to the user's prompt using the Gemini model.

    Args:
        user_prompt (str): The user's prompt or question.

    Returns:
        str: The generated response.
    """
    # Define the system message for the generative model
    system_message = input("System Message: ")

    # Set the Google API key (use environment variable if available, otherwise use hardcoded key)
    gog_key = input("Google API Key: ")

    # Load environment variables from .env file
    load_dotenv()

    # Set the Google API key environment variable
    os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY', gog_key)

    # Configure the Google Generative AI library
    google.generativeai.configure()

    # Create a Gemini model instance with the system instruction
    gemini = google.generativeai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=system_message
    )

    # Generate content using the Gemini model
    response = gemini.generate_content(user_prompt)

    # Return the generated response text
    return response.text