
from flask import Flask, render_template, request, session, jsonify  

from openai import OpenAI
import os

app = Flask(__name__)
app.secret_key = 'assistant-ai-1a-urrugne-64122'  # Définissez une clé secrète pour les sessions

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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
    
    # return render_template('index.html', messages=message_history)
    return jsonify({"response": response_chatgpt})

if __name__ == '__main__':
    app.run(debug=True)
