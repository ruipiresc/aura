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
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_BOT_OWNER_ID = os.getenv("SLACK_BOT_OWNER_ID")

# Set URLs for Telegram and Slack APIs
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
SLACK_API_URL = "https://slack.com/api"

@app.route('/')
def home():
    return "Aura Bot is running on version " + get_version()

@app.route('/webhook', methods=['POST'])
def webhook():
    # Get the incoming request data
    data = request.get_json()

    if "message" in data:  # Telegram webhook data
        return handle_telegram_webhook(data)
    elif "event" in data:  # Slack webhook data
        return handle_slack_webhook(data)
    else:
        return "Unsupported webhook source", 400

def handle_telegram_webhook(data):
    # Extract the chat ID and text from the incoming message
    chat_id = data['message']['chat']['id']
    text = data['message']['text']
    user_id = data["message"]["from"]["id"]  # Extract user ID
    print(f"Telegram User ID: {user_id}")  # Print the user ID to the console

    # Echo the message back to the user in Telegram and Slack
    send_message_to_telegram(chat_id, text)
    send_message_to_slack(SLACK_BOT_OWNER_ID, text)

    return '', 200

def handle_slack_webhook(data):
    # Extract the text and channel from the incoming message
    event = data.get('event', {})
    text = event.get('text', '')
    user_id = event.get('user', '')
    channel = event.get('channel', '')
    subtype = event.get('subtype', '')
    print(f"Slack User ID: {user_id}, Channel: {channel}")
    
    # Ignore messages sent by the bot itself (using the 'subtype' field)
    if subtype != 'bot_message':
        # Echo the message back to Slack
        send_message_to_slack(channel, text)

    return '', 200

def send_message_to_telegram(chat_id, text):
    """Send a message back to the user via Telegram."""
    url = f"{TELEGRAM_API_URL}/sendMessage"
    params = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, params=params)

    if response.status_code != 200:
        print(f"Error sending Telegram message: {response.text}")

def send_message_to_slack(channel, text):
    """Send a message to the specified Slack channel."""
    url = f"{SLACK_API_URL}/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": channel,
        "text": text
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200 or not response.json().get("ok"):
        print(f"Error sending Slack message: {response.text}")

if __name__ == '__main__':
    send_message_to_telegram(TELEGRAM_BOT_OWNER_ID, "Aura is now online and ready on version " + get_version())
    send_message_to_slack(SLACK_BOT_OWNER_ID, "Aura is now online and ready on version " + get_version())

    app.run(debug=True, host="0.0.0.0", port=5080)
