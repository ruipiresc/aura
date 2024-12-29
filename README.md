# Aura: Your Personal Telegram Assistant Bot

**Aura** is a personal assistant bot built for Telegram, designed to assist you with simple tasks through text-based interactions. Using Python and Flask, it operates with a webhook-based architecture to provide real-time message handling. Aura runs 24/7 on Cyclic and is perfect for personal use and automation.

## Features
- Echo bot functionality for quick responses.
- Built with **Python** and **Flask**.
- Hosted on **Cyclic** for continuous availability.
- Secure handling of secrets with environment variables.
- Webhook integration with the **Telegram API** for real-time updates.

## Getting Started

Follow the steps below to get started with Aura on your local machine and deploy it to Cyclic.

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/aura.git
cd aura
```

### 2. Set Up Your Environment

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### 3. Set Up Telegram Bot

- Go to [@BotFather](https://core.telegram.org/bots#botfather) on Telegram and create a new bot.
- Note the API token provided by BotFather.

### 4. Running Locally with Ngrok

To run the bot locally and use webhooks, you can expose your local server using [ngrok](https://ngrok.com/):

1. Download and install ngrok.
2. Start your Flask app:

```bash
python app.py
```

3. Start ngrok:

```bash
ngrok http 5000
```

4. Copy the HTTPS URL provided by ngrok and set it as your webhook in the Telegram Bot API:

```bash
curl -F "url=https://your-ngrok-url" https://api.telegram.org/bot<your-bot-token>/setWebhook
```

### 5. Deploy to Cyclic

To deploy your bot to Cyclic:

1. Create an account on [Cyclic](https://cyclic.sh/).
2. Create a new app and connect it to your GitHub repository.
3. Set up environment variables for your secrets in the Cyclic dashboard (e.g., `TELEGRAM_TOKEN`).
4. Cyclic will automatically deploy your app when you push changes to `main`.

### 6. Accessing the Bot

Once deployed, your bot should start responding to messages in Telegram. Just type any message to start the echo functionality.

## License

This project is licensed under the MIT License with a restriction on commercial use. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Telegram Bot API](https://core.telegram.org/bots/api) for the messaging platform.
- [Flask](https://flask.palletsprojects.com/) for the web framework.
- [Cyclic](https://cyclic.sh/) for the cloud hosting.

---

Feel free to open an issue or pull request if you have suggestions or improvements!