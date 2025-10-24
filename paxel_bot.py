from flask import Flask, request
from twilio.rest import Client
import json
import threading
import time

# === CONFIGURATION TWILIO ===
account_sid = 'AC229e9b5ba22977d241cb5777a1150b8d'
auth_token = '2758279ec1be5b3408fe6092e5022c9b'
client = Client(account_sid, auth_token)

twilio_whatsapp_number = 'whatsapp:+14155238886'
template_sid = 'HXb5b62575e6e4ff6129ad7c8efe1f983e'  # ton Content Template SID

# === RESPONSES PAR CONTACT ===
responses = {
    '+33758080294': {
        "1": "Mes salutations au pere de mon createur, Je suis Paxel une IA cree par Karlito pour repondre a ses messages quand il n'est pas disponible.",
        "2": "Pour l'instant votre fils n'est pas disponible quand il le saura il repondra a votre message."
    },
    '+18092820899': {
        "1": "Pour l'instant Karlito n'est pas disponible, vu que tu est sa meuilleure amie il te repondra vite quand il verra ton message.",
        "2": "Je suis Paxel son AI assistant cree pour repondre a ses messages a sa place."
    },
    '+18097520703': {
        "1": "Je t'ecrirais quand je serais disponible",
        "2": "bby"
    },
    '+50938576922': {
        "1": "Je suis Paxel le chatbot de Karlito, si je reponds a ton message a sa place c'est que il n'est pas disponible pour l'instant.",
        "2": "Quand il sera disponible il te repondra."
    },
    '+18493957350': {
        "1": "Hola Kim, soy Paxel, el chatbot de Karlito.",
        "2": "Si yo respondo tus mensajes en lugar de él, es porque no está disponible en este momento. En cuanto esté disponible, te responderá."
    }
}

# Message par défaut pour les autres
default_response = {
    "1": "Karlito n'est pas disponible pour l'instant il entrera en contact avec vous quand il sera disponible.",
    "2": "Je suis Paxel son Chatbot cree pour repondre a sa place."
}

# === FLASK APP ===
app = Flask(__name__)

def send_whatsapp_response(to_number):
    time.sleep(30)  # délai de 30 secondes
    variables = responses.get(to_number, default_response)
    message = client.messages.create(
        from_=twilio_whatsapp_number,
        to='whatsapp:' + to_number,
        content_sid=template_sid,
        content_variables=json.dumps(variables)
    )
    print(f"Message envoyé à {to_number}: {message.sid}")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.form
    from_number = data.get('From').replace('whatsapp:', '')
    
    # On envoie la réponse dans un thread pour ne pas bloquer Twilio
    threading.Thread(target=send_whatsapp_response, args=(from_number,)).start()
    
    return "OK", 200

if __name__ == "__main__":
    # Port recommandé pour Render
    app.run(host="0.0.0.0", port=5000)
