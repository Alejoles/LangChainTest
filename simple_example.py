from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

# por defecto el modelo que se usa es gpt-3.5-turbo
chat_model = ChatOpenAI(model="gpt-3.5-turbo", api_key=API_KEY)

result = chat_model.invoke("Hola!")

print(result)