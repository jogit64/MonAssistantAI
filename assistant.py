from flask import Flask, render_template, request, session, jsonify
from flask_cors import CORS
from openai import OpenAI
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
CORS(app)
app.secret_key = 'assistant-ai-1a-urrugne-64122'

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://lebonubw:Baltimore69@lebonubw/lebonubw.mysql.db')
db = SQLAlchemy(app)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_key = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

@app.route('/')
def home():
    session['message_history'] = []  # Réinitialise l'historique pour chaque nouvelle session
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    question = request.form['question']
    
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

    # Log user question
    new_message = Message(session_key=session['message_key'], message=question, role='user')
    db.session.add(new_message)
    db.session.commit()
    
    # Log GPT response
    response_message = Message(session_key=session['message_key'], message=response_chatgpt, role='assistant')
    db.session.add(response_message)
    db.session.commit()
    
    return jsonify({"response": response_chatgpt})

if __name__ == '__main__':
    app.run(debug=True)
