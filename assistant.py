from flask import Flask, render_template, request, session, jsonify
from flask_cors import CORS
from openai import OpenAI
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS



app = Flask(__name__)
CORS(app, supports_credentials=True, origins=['https://www.goodyesterday.com'])
# CORS(app)
app.secret_key = 'assistant-ai-1a-urrugne-64122'  # Définissez une clé secrète pour les sessions


app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'None'

# Initialisez l'extension Flask-Session ou une autre gestion de session ici...
# Session(app)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Configuration OpenAI
openai_api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# Initialisation de SQLAlchemy
db = SQLAlchemy(app)

# Définition du modèle de message
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_key = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Route principale
@app.route('/')
def home():
    session['message_history'] = []  # Réinitialise l'historique pour chaque nouvelle session
    return render_template('index.html')

# Route pour poser une question
@app.route('/ask', methods=['POST'])
def ask_question():
    question = request.form['question']
    session_key = request.form['sessionKey']  # Récupère la clé de session à partir des données de la requête
    
    # Récupère l'historique des messages de la session actuelle
    message_history = session.get('message_history', [])
    
    # Ajoute la nouvelle question à l'historique des messages de la session
    message_history.append({"role": "user", "content": question})
    
    # Envoie la requête avec l'historique des messages de la session
    chat_completion = client.chat.completions.create(
        messages=message_history,
        model="gpt-3.5-turbo",
    )
    
    # Récupère la réponse de l'API 
    response_chatgpt = chat_completion.choices[0].message.content
    
    # Ajoute la réponse à l'historique des messages de la session
    message_history.append({"role": "assistant", "content": response_chatgpt})
    
    # Sauvegarde l'historique mis à jour dans la session
    session['message_history'] = message_history

     # Indique explicitement que la session a été modifiée
    session.modified = True
    
    # return render_template('index.html', messages=message_history)
    return jsonify({"response": response_chatgpt})

    # Log user question
    new_message = Message(session_key=session_key, message=question, role='user')  # Utilise session_key
    db.session.add(new_message)
    db.session.commit()
    
    # Log GPT response
    response_message = Message(session_key=session_key, message=response_chatgpt, role='assistant')  # Utilise session_key
    db.session.add(response_message)
    db.session.commit()
    
    return jsonify({"response": response_chatgpt})
