# LangChain

---

<aside>
📝 LangChain es un FrameWork creado para Python y JS que sirve para crear aplicaciones con Inteligencia Artificial

</aside>

<aside>
📝 [Tutorials | 🦜️🔗 LangChain](https://python.langchain.com/v0.2/docs/tutorials/)

</aside>

---

# Instalación

Solían haber 3 formas para instalar Langchain pero ahora únicamente se debe de correr un comando que es el siguiente:

- **pip install langchain** instala los requerimientos mínimos de langchain para poder correrlo en una máquina.

```bash
pip install langchain
```

Adicionalmente para este ejemplo se instalarán los paquetes para que se pueda operar con OpenAI (ChatGPT).

```bash
pip install langchain_openai
```

Todo lo anterior lo podremos instalar del repositorio: https://github.com/Alejoles/LangChainTest

### LINUX

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows

```bash
python -m vevn venv
cd venv/Scripts && activate && cd ../../
pip install -r requirements.txt
```

Finalmente creamos un nuevo archivo .env y configuramos las variables de entorno que se encuentran dentro del archivo .env.example

Para crear una api-key ingresa a [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys).

A continuación veremos 5 ejemplos, cada uno un poco más complejo que el anterior.

# Ejemplos

## Ejemplo 1 (Inicial).

Con el siguiente ejemplo podemos mirar un poco el funcionamiento de LangChain.

```python
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

# por defecto el modelo que se usa es gpt-3.5-turbo
chat_model = ChatOpenAI(model="gpt-3.5-turbo", api_key=API_KEY)

result = chat_model.invoke("Hola!")

print(result)
```

Si ejecutamos el ejemplo anterior nos debería de devolver algo como:  **content**=“¡Hola! ¿En qué puedo ayudarte hoy?” y otros objetos como **response_metadata**, **id** y **usage_metadata**

## Ejemplo 2 (Mensajes múltiples).

En este ejemplo veremos cómo se envían varios mensajes y que estén en el mismo prompt para que responda de acuerdo a mensajes anteriores.

```python
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
```

## Ejemplo 3 (Prompt Template).

Un prompt template es una plantilla que se le indica al modelo para que siga ciertas reglas que se le imponen, por ejemplo le podemos decir al modelo que sea un traductor que traduce de un lenguaje a otro como en el siguiente ejemplo:

```python
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
```

Ya viendo el ejemplo anterior podemos decirle que de cualquier lenguaje traduzca a español o lo que se requiera.

Para tener en cuenta:

- Los textos que se encuentran dentro de llaves “{}” en los strings son los inputs que recibe el método format_messages(), es decir pueden cambiar a conveniencia del programador.
- Pueden haber 3 tipos de mensaje dentro de from_messages(), estos serían **system, ia** y **human.**
- Podemos encontrar más acerca de este tema dentro de https://python.langchain.com/v0.1/docs/modules/model_io/prompts/quick_start/

## Ejemplo 4 (Output Parser).

Lo que haremos en este ejemplo es realizar un parser, entonces lo que queremos es separar la charla adicional que da el modelo de la respuesta que queremos, para esto usaremos todo lo aprendido anteriormente.

```python
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
```

## Ejemplo 5 (Chain).

Veremos un ejemplo de una cadena y de por qué se llama langchain el framework

```python
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
```

Para ser un poco más explícitos, la cadena indica el orden en el que se hacen las cosas y para esto usamos el operador “|” que en la sintaxis de langchain funciona para realizar la cadena.

```python
chain = chat_prompt | chat_model | CommaSeparatedListOutputParser()
result = chain.invoke({"text": "colors"})
```

En primera instancia se crea el prompt que sería el template que se le envía al modelo, por ende lo segundo que se realiza es entrenar el modelo y finalmente se hace un parsing a la respuesta que da el modelo y obtenemos lo que necesitamos.

- Le pasamos el chat generado por el template.
- Se lo pasamos al modelo para entrenarlo.
- Y pasamos la respuesta al parser.
- Finalmente obtenemos respuesta.

# SQL

<aside>
📝 [SQL Database | 🦜️🔗 LangChain](https://python.langchain.com/v0.2/docs/integrations/toolkits/sql_database/)

</aside>

LangChain se puede conectar a fuentes de datos, como bases de datos.

Lo que podemos hacer es que se conecte a una base de datos y con lenguaje natural pedirle que haga querys y nos de un resultado. CUIDADO, los prompts pueden llegar a modificar la base de datos por lo que siempre hay que tener cuidado con datos sensibles, siempre debemos tener una copia de seguridad y evitar dar permisos de escritura a una base de datos que le pasamos al modelo.

# Ejemplo de como crear un sistema de preguntas y respuestas con una base de datos SQL

<aside>
📝 [Build a Question/Answering system over SQL data | 🦜️🔗 LangChain](https://python.langchain.com/v0.2/docs/tutorials/sql_qa/#chains)

</aside>

# Herramientas interesantes

<aside>
📝 [Hugging Face | 🦜️🔗 LangChain](https://python.langchain.com/v0.2/docs/integrations/platforms/huggingface/)

</aside>