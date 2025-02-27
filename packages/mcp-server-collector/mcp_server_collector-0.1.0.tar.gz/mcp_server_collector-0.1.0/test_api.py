import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize client
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_BASE_URL')
)

# Test API connection
try:
    response = client.chat.completions.create(
        model=os.getenv('OPENAI_MODEL'),
        messages=[
            {"role": "user", "content": "Hello, how are you?"}
        ]
    )
    print("API connection successful!")
    print("Response:", response.choices[0].message.content)
except Exception as e:
    print("API Error:", str(e))