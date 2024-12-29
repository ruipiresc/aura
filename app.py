import os
import requests
from flask import Flask, request
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get your Telegram bot token from environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

@app.route('/')
def home():
    return "Aura Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    # Get the message from the Telegram API
    data = request.get_json()

    # Extract the chat ID and text from the incoming message
    chat_id = data['message']['chat']['id']
    text = data['message']['text']
    
    # print the message
    print(f"Message from {chat_id}: {text}")

    # Echo the message back to the user
    send_message(chat_id, text)

    return '', 200

def send_message(chat_id, text):
    """Send a message back to the user via Telegram"""
    url = f"{TELEGRAM_API_URL}/sendMessage"
    params = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, params=params)

    if response.status_code != 200:
        print(f"Error sending message: {response.text}")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5080)
