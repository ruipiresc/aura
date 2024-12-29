import os
import requests
from flask import Flask, request

def get_version():
    with open("VERSION") as f:
        return f.read().strip()

app = Flask(__name__)

# Load environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_BOT_OWNER_ID = os.getenv("TELEGRAM_BOT_OWNER_ID")

# Set url for Telegram API
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

@app.route('/')
def home():
    return "Aura Bot is running on version " + get_version()

@app.route('/webhook', methods=['POST'])
def webhook():
    # Get the message from the Telegram API
    data = request.get_json()

    # Extract the chat ID and text from the incoming message
    chat_id = data['message']['chat']['id']
    text = data['message']['text']
    user_id = data["message"]["from"]["id"]  # Extract user ID
    print(f"User ID: {user_id}")  # Print the user ID to the console

    # Echo the message back to the user
    send_message(chat_id, text)

    return '', 200

def send_message(chat_id, text):
    """Send a message back to the user via Telegram."""
    url = f"{TELEGRAM_API_URL}/sendMessage"
    params = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, params=params)

    if response.status_code != 200:
        print(f"Error sending message: {response.text}")

if __name__ == '__main__':
    send_message(TELEGRAM_BOT_OWNER_ID, "Aura is now online and ready on version " + get_version())
    
    app.run(debug=True, host="0.0.0.0", port=5080)
