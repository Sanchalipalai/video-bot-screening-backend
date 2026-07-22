import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    models = client.models.list()
    print("SUCCESS!")
    print(models.data[0].id)
except Exception as e:
    print(type(e).__name__)
    print(e)