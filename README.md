# Discord Bot Setup

## Introduction
This repository contains the source code for a Discord bot using `disnake`. Before running the bot, you'll need to set up a few things, including your bot's token which is used to authenticate your bot with the Discord API.

## Prerequisites
- Python 3.8+ (recommended: 3.8+)
- `disnake` library installed
- `.env` file to store your sensitive configuration values (like the bot's token)

## Setting up the bot

### 1. Clone the repository
Clone the repository to your local machine using the following command:
```powershell
git clone "https://github.com/laibz9/astoria_botv3"
cd "<your-repository-directory>"
```
### 2. Install dependencies
Install the required Python libraries by running the following:
```powershell
pip install -r requirements.txt
```
### 3. Create a `.env` file in the `config` folder
In the root of the project, create a folder named `config` if it does not exist already. Inside the `config` folder, create a file named `.env` and add the following content:
#### Example `.env` File:
```.env
TOKEN=your_discord_bot_token_here
```
**Note:** Replace `your_discord_bot_token_here` with your actual bot token. You can get your token from the [Discord Developer Portal](https://discord.com/developers/applications).
#### Folder Structure Example:
```python
/project-root ├── /config
              │ ├── .env <-- Your bot token goes here
              ├── /cogs
              ├── bot.py
              ├── requirements.txt
              └── README.md
```
### 4. Load the Token in Your Code
In your bot's code (for example, `bot.py`), you will need to load the token from the `.env` file. This can be done using the `python-dotenv` library.
First, install the `python-dotenv` library:
```powershell
pip install python-dotenv
```
### 5. Run the bot
After setting up the .env file and loading the token in your bot's code, you can run the bot:
```python
python bot.py
```
If everything is set up correctly, your bot should start up and be ready to use!
## Troubleshooting
- Bot not starting: Double-check that the `.env` file is in the correct location (`config/.env`) and that the TOKEN variable is correctly set in that file.
- Missing dependencies: Make sure to install all required dependencies using `pip install -r requirements.txt`.