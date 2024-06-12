from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import BaseOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

class AnswerOutputParser(BaseOutputParser):
    def parse(self, text: str):
        """ Parse the output of an LLM call. """
        return text.strip().split("respuesta =")

# por defecto el modelo que se usa es gpt-3.5-turbo
chat_model = ChatOpenAI(model="gpt-3.5-turbo", api_key=API_KEY)

template = """Eres un asistente que resuelve problemas de matemáticas y enseñas tu trabajo.
              Da la salida de cada paso y luego retorna siempre la respuesta en el siguiente formato: respuesta = <respuesta acá>.
              Asegurate de siempre al dar la respuesta escribir respuesta = <dar la respuesta en este espacio>.
              Asegurate de escribir respuesta siempre en minusculas y que tenga exactamente un espacio y un signo de igual despues del espacio.
           """
human_template = "{problem}"

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", human_template)
])

message = chat_prompt.format_messages(problem="2x^2 - 5x + 3 = 0")

result = chat_model.invoke(message)

# Acá empieza la parte de hacer parsing
parsed = AnswerOutputParser().parse(result.content)
steps, answer = parsed

print(answer)