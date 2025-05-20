from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

# Function to generate response from GPT-4
def generate_gpt4_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return None

result = generate_gpt4_response("Hello, how are you?")
print(result)