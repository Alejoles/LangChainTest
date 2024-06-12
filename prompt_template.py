from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

# por defecto el modelo que se usa es gpt-3.5-turbo
chat_model = ChatOpenAI(model="gpt-3.5-turbo", api_key=API_KEY)

template = "Eres un asistente que traduce de {input_language} a {output_language}."
human_template = "{human_text}"

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", human_template)
])

message = chat_prompt.format_messages(input_language="Spanish",
                                       output_language="Portuguese",
                                       human_text="En realidad amo programar.")

result = chat_model.invoke(message)

print(result)