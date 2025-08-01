
from fastapi import FastAPI #pip install "fastapi[standard]"
from fastapi.middleware.cors import CORSMiddleware

# Get the API key from here: https://ai.google.dev/tutorials/setup
# Create a new secret called "GEMINI_API_KEY", via Add-ons/Secrets in the top menu, and attach it to this notebook
import google.generativeai as genai # pip install google-generativeai


from dotenv import load_dotenv #pip install python-dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the variables
api_key = os.getenv('API_KEY')

genai.configure(api_key = api_key)

# Generate content model
model = genai.GenerativeModel(model_name='gemini-1.5-flash-latest')
app = FastAPI()

# Configuraci  n de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier origen
    allow_credentials=True,  # Si necesitas cookies o credenciales
    allow_methods=["*"],  # Permite todos los m  todos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todas las cabeceras
)

@app.get("/recetas/generar")
def generarRecetas(tipo: str):

    prompt = """Dame recetas del siguiente tipo:"""+tipo+""" en formato JSON.

    Usa este esquema JSON schema:

    Receta = {'receta_nombre': str, 'ingredientes': list[str]}
    Return: list[Recipe]"""

    response = model.generate_content(prompt)
    print(response.text)
    # Use the response as a JSON string.
    return response.text
