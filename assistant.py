from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Charge les variables d'environnement du fichier .env
load_dotenv()

# Initialisation du client OpenAI avec votre clé API
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Variable globale pour stocker l'historique des messages
global_message_history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    question = request.form['question']
    
    # Ajouter la nouvelle question à l'historique des messages
    global global_message_history
    global_message_history.append({"role": "user", "content": question})
    
    # Envoie la requête avec l'historique des messages
    chat_completion = client.chat.completions.create(
        messages=global_message_history,
        model="gpt-3.5-turbo",
    )
    
    # Récupérer la réponse de l'API
    response_chatgpt = chat_completion.choices[0].message.content
    
    # Ajouter la réponse à l'historique des messages
    global_message_history.append({"role": "assistant", "content": response_chatgpt})
    
    return render_template('index.html', messages=global_message_history)

if __name__ == '__main__':
    app.run(debug=True)
