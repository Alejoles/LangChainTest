from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import BaseOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

# por defecto el modelo que se usa es gpt-3.5-turbo
chat_model = ChatOpenAI(model="gpt-3.5-turbo", api_key=API_KEY)

class CommaSeparatedListOutputParser(BaseOutputParser):
    def parse(self, text: str):
        """ Parse the output of an LLM call. """
        return text.strip().split(", ")

template = """Eres es un útil asistente que genera listas separadas por comas.
              Un usuario te pasa una categoría y debes generar 5 objetos de esa categoría en una lista separada por comas.
              SOLO devuelve una lista separada por comas y nada más.
           """
# este {text} se va a ingresar luego en la cadena (chain)
human_template = "{text}"

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", human_template)
])

# CHAIN
chain = chat_prompt | chat_model | CommaSeparatedListOutputParser()
# El text es del template que se realizó en la línea 24
result = chain.invoke({"text": "colors"})
print(result)