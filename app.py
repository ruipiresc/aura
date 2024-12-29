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
    # Extract the chat ID, text, and user info from the incoming message
    chat_id = data['message']['chat']['id']
    text = data['message']['text']
    user_id = data["message"]["from"]["id"]  # Extract user ID
    username = data["message"]["from"].get("username", data["message"]["from"].get("first_name", "User"))  # Fallback to first_name if no username

    # Avoid responding to the bot's own messages or messages from 'Lola'
    if user_id == int(TELEGRAM_BOT_OWNER_ID) or username.lower() == "lola":
        return '', 200  # Ignore bot's own messages and messages from "Lola"

    # Format the message
    formatted_message = f"You ({username}) said: {text}"

    # Echo the formatted message back to Telegram and Slack
    send_message_to_telegram(chat_id, formatted_message)
    send_message_to_slack(SLACK_BOT_OWNER_ID, formatted_message)

    return '', 200

def handle_slack_webhook(data):
    # Extract the text, user, and subtype from the incoming Slack message
    event = data.get('event', {})
    text = event.get('text', '')
    user_id = event.get('user', '')
    channel = event.get('channel', '')
    subtype = event.get('subtype', '')

    # Avoid responding to the bot's own messages or messages from 'Lola'
    if subtype == 'bot_message':  # Check if the message is sent by the bot
        return '', 200  # Ignore bot's own messages

    # Get the user's name or username from Slack API
    user_info = get_slack_user_info(user_id)
    username = user_info.get("real_name", "User")  # Use real_name if available, fallback to "User"

    # Avoid responding to messages from 'Lola'
    if username.lower() == "lola":
        return '', 200  # Skip if the username is "Lola"

    # Format the message
    formatted_message = f"You ({username}) said: {text}"

    # Echo the formatted message back to Slack
    send_message_to_slack(channel, formatted_message)

    return '', 200

def get_slack_user_info(user_id):
    """Fetch user information from Slack API."""
    url = f"{SLACK_API_URL}/users.info"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    params = {
        "user": user_id
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json().get("user", {})
    else:
        print(f"Error fetching Slack user info: {response.text}")
        return {}

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
    else:
        print(f"Slack message sent successfully: {text}")

if __name__ == '__main__':
    # Ensure the bot sends an initial message to both Telegram and Slack on startup
    send_message_to_telegram(TELEGRAM_BOT_OWNER_ID, "Aura is now online and ready on version " + get_version())
    
    # Log the result of sending a message to Slack
    slack_message = "Aura is now online and ready on version " + get_version()
    send_message_to_slack(SLACK_BOT_OWNER_ID, slack_message)

    app.run(debug=True, host="0.0.0.0", port=5080)
