# Shenanigan-bot

A small Discord bot that uses ChatGPT to send an obscure / entertaining message every 24 hours (or on demand via a slash command). Built in Python. 
Add bot: https://discord.com/oauth2/authorize?client_id=1446220110363885578

## Features

- Sends an automated "shenanigan" message once every 24 hours.
- Responds to a slash command to generate an on-demand message via ChatGPT.
- Modular structure with a commands folder to add more commands.
- Simple task scheduler for recurring messages.

## Files 

- `bot.py` — Bot entrypoint and Discord client initialization.
- `ai.py` — ChatGPT / AI helper utilities.
- `tasks.py` — Scheduled tasks (24-hour message).
- `extensions.py` — Bot extension/utility loading.
- `commands/` — Directory for command modules (slash commands).
- `requirements.txt` — Python dependencies.

## Prerequisites

- Python 3.10+ recommended
- A Discord bot token with the appropriate gateway and application command permissions
- An OpenAI API key (or whichever ChatGPT/LLM provider the `ai.py` helper expects)

## Installation

1. Clone the repository (or copy files into your environment):

   git clone https://github.com/MicahXX/Shenanigan-bot.git
   cd Shenanigan-bot

2. Create and activate a virtual environment:

   python -m venv .venv
   source .venv/bin/activate  # macOS / Linux
   .venv\Scripts\activate     # Windows

3. Install dependencies:

   pip install -r requirements.txt

## Configuration

Create a `.env` file or export environment variables required by the bot. Typical environment variables used by this project:

- DISCORD_TOKEN — Your Discord bot token.
- OPENAI_API_KEY — API key for the ChatGPT/OpenAI integration.

Example `.env`:

DISCORD_TOKEN=your_discord_token_here
OPENAI_API_KEY=your_openai_key_here

## Usage

Start the bot:

python bot.py

What the bot does after startup:

- Registers (or ensures) slash commands are available (if implemented in `commands/`).
- Loads extensions and scheduled tasks.
- Sends out an automated "shenanigan" message once every 24 hours (implemented in `tasks.py`).
- Responds to slash command(s) to generate an on-demand message via the AI helper.

Example (if a slash command `/shenanigan` exists):
- Type `/shenanigan` in the server where the bot is present to receive an immediate generated message.

## Development notes

- Add new slash commands by creating modules in the `commands/` directory.
- `ai.py` contains the integration with the language model — adjust prompt templates and parameters there.
- `tasks.py` manages the scheduled job; change frequency or behavior there.
- The repository is private and currently does not include a license file.

## Deployment

- Run the bot on any persistent host (VM, container, serverless platform with websockets support).
- Consider Dockerizing the app or running under a process manager (systemd, supervisord) to keep it running.
- Ensure environment variables are injected securely (secrets manager, environment vars).

## Troubleshooting

- Bot fails to connect: verify `DISCORD_TOKEN` and bot permissions (gateway intents if required).
- Slash commands not appearing: ensure the bot has the applications.commands scope and the correct guild (or global registration) flow. Give it some time if registering globally.
- AI calls failing: confirm `OPENAI_API_KEY` and that rate limits/quotas are not exceeded.

## Contributing

- Open an issue describing the feature or bug.
- Add commands in `commands/` and open a pull request.
- Keep changes focused and include tests where appropriate.

## Author

Made by MicahCode(MicahXX)
