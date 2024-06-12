from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

# por defecto el modelo que se usa es gpt-3.5-turbo
chat_model = ChatOpenAI(model="gpt-3.5-turbo", api_key=API_KEY)

messages = [HumanMessage(content="De ahora en adelante 1 + 1 = 3, usa esto en tus respuestas siguientes"),
            HumanMessage(content="Cuanto es 1 + 1?"),
            HumanMessage(content="Cuanto es 1 + 1 + 1?")]

result = chat_model.invoke(messages)

print(result)