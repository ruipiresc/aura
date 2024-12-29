# Aura - Personal Assistant Bot

Aura is a simple Telegram bot designed to act as a personal assistant. It is built using Python, Flask, and runs on a webhook to listen for incoming messages. This bot is a work in progress and can be easily extended to suit different needs.

## Features

- **TODO**: TODO.

## Prerequisites

- Python 3.x
- Flask
- Requests
- A Telegram bot token

## Installation

### Step 1: Clone the repository
Clone this repository to your local machine.

```bash
git clone https://github.com/ruipiresc/aura.git
cd aura
```

### Step 2: Create a Python virtual environment (optional but recommended)
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install dependencies
Install required Python packages.

```bash
pip install -r requirements.txt
```

### Step 4: Set up your `.env` file
Create a `.env` file in the root directory with the following values:

```
TELEGRAM_BOT_TOKEN=<your-telegram-bot-token>
TELEGRAM_BOT_OWNER_ID=<your-telegram-user-id>
```

Replace `<your-telegram-bot-token>` with the bot token you received from @BotFather, and `<your-telegram-user-id>` with your Telegram user ID (can be obtained via the `userinfobot` on Telegram).

### Step 5: Run the bot locally
To run the bot locally with a webhook, use `ngrok` to expose your local server to the internet.

1. Start your Flask app:

   ```bash
   python app.py
   ```

2. In a separate terminal, start `ngrok`:

   ```bash
   ngrok http 5000
   ```

   Copy the HTTPS URL provided by `ngrok`.

3. Set the webhook for your bot using the following curl command, replacing `<your-ngrok-url>` with the URL you got from `ngrok`:

   ```bash
   curl -X POST "https://api.telegram.org/bot<your-telegram-bot-token>/setWebhook?url=<your-ngrok-url>/webhook"
   ```

### Step 6: Interact with your bot
Now you can send messages to your bot. It will only respond to messages from the user defined in `TELEGRAM_BOT_OWNER_ID`.

---

## Version Management

We follow Semantic Versioning for this project. Here’s how versioning is handled:

- **Patch version**: Incremented for bug fixes or minor improvements.
- **Minor version**: Incremented for adding new features in a backward-compatible manner.
- **Major version**: Incremented for breaking changes.

You can bump the version manually using the `bump_version.py` script.

### Usage of Version Bumping Script

#### Step 1: Update Version and Changelog

You can manually bump the version (patch, minor, or major) with the following command:

```bash
python bump_version.py <bump_type> "<changelog_message>"
```

- **bump_type** can be one of: `patch`, `minor`, or `major`.
- **changelog_message** should be a short description of the changes you made.

Example:

```bash
python bump_version.py patch "Fixed bug in authentication flow"
```

#### Step 2: Git Operations

The script will automatically:

1. Increment the version number.
2. Update the `CHANGELOG.md` file.
3. Commit the changes.
4. Create a Git tag for the version.
5. Push the commit and tag to the remote repository.

---

## Deployment

This project is now deployed on [Railway](https://railway.app/). Follow these steps to deploy the bot on Railway:

1. Create an account on Railway and log in.
2. Create a new project and select **GitHub** as the deployment source.
3. Link your GitHub repository to Railway.
4. Set up your environment variables (`TELEGRAM_BOT_TOKEN` and `TELEGRAM_BOT_OWNER_ID`) on Railway:
   - Go to the **Settings** tab of your project.
   - Add the required environment variables under the **Environment Variables** section.
5. Railway will automatically deploy your bot whenever you push changes to your repository.

---

## Contribution

Feel free to fork this project and submit pull requests. If you want to contribute, ensure that you follow the versioning and changelog conventions.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.