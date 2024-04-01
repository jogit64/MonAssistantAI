import os
from openai import OpenAI
from dotenv import load_dotenv

# Charge les variables d'environnement du fichier .env
load_dotenv()

# Initialisation du client OpenAI avec votre clé API
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# On déclare une liste pour conserver l'historique de tous nos messages avec ChatGPT
messages = []

# Optionnel, permet de définir le comportement que l'assistant doit adopter
messages.append({"role": "system", "content": "Tu es assistant astronome."})

# Une question classique qu'on pourrait poser à ChatGPT
messages.append({"role": "user", "content": "Quelle est la distance entre la terre et le lune ?"})

# Envoie la requête avec l'historique des messages
chat_completion = client.chat.completions.create(
    messages=messages,
    model="gpt-3.5-turbo",
)

# Affiche la réponse de l'API
response_chatgpt = chat_completion.choices[0].message.content
print(response_chatgpt)



# On inclut la réponse dans l'historique des messages
messages.append({"role": "assistant", "content": response_chatgpt})

# Je pose une nouvelle question
messages.append({"role": "user", "content": "Et jupiter ?"})

# Envoie la requête avec l'historique des messages mis à jour
chat_completion = client.chat.completions.create(
    messages=messages,
    model="gpt-3.5-turbo",
)

# Affiche la nouvelle réponse de l'API
response_chatgpt = chat_completion.choices[0].message.content
print(response_chatgpt)
