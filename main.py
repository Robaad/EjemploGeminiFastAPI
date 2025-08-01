from flask import Flask, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
import os
from flask_cors import CORS

# Cargar variables de entorno
load_dotenv()
api_key = os.getenv('API_KEY')
genai.configure(api_key=api_key)

# Crear modelo de Gemini
model = genai.GenerativeModel(model_name='gemini-1.5-flash-latest')

# Crear app Flask
app = Flask(__name__)
CORS(app)  # Habilita CORS para todos los orígenes

@app.route('/recetas/generar', methods=['GET'])
def generar_recetas():
    tipo = request.args.get('tipo')
    if not tipo:
        return jsonify({"error": "Falta el parámetro 'tipo'"}), 400

    prompt = f"""Dame recetas del siguiente tipo: {tipo} en formato JSON.

    Usa este esquema JSON schema:

    Receta = {{'receta_nombre': str, 'ingredientes': list[str]}}
    Return: list[Recipe]
    """

    try:
        response = model.generate_content(prompt)
        return jsonify({"respuesta": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
