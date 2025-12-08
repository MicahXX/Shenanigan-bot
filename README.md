# Shenanigan-bot

A modular Discord bot using ChatGPT/gpt-4o to deliver hilarious, obscure, and custom AI messages on demand or automatically. Built in Python.  
Add bot: https://discord.com/oauth2/authorize?client_id=1446220110363885578

## Features

- Sends an automated "shenanigan" message once every 24 hours (default: off).
- Can be used to just prompt the ai.
- Extensive admin commands to control scheduling, content, and delivery.
- Simple task scheduler for recurring and custom-timed events.
- Supports setting the prompt, frequency, channel, and message uniqueness threshold.
- Uses gpt-4o via OpenAI for responses.
- Admin-only commands for configuration and testing.

## Files 

- `bot.py` — Entrypoint and Discord client initialization.
- `ai.py` — ChatGPT/OpenAI integration and AI helper utilities.
- `tasks.py` — Scheduled tasks (24-hour and custom interval messages).
- `extensions.py` — Extension and command loader.
- `commands/` — Slash command modules.
- `requirements.txt` — Python dependencies.
- `utils/` — Helper utilities (e.g. settings storage).

## Slash Commands

**/outrageous**  
Get a random, wild, or funny AI-generated message.

**/prompt [text]**  
Send a custom prompt to ChatGPT (gpt-4o).

**/daily_enable**  
Enable daily automated messages for this server (admin only).

**/daily_disable**  
Disable daily automated messages for this server (admin only).

**/daily_status**  
Show the current daily message settings for your server, including enabled state, interval, prompt, channel mode, channel, and uniqueness threshold (admin only).

**/daily_test**  
Send the daily message immediately (useful for testing configurations, admin only).

**/daily_customtime [interval]**  
Set how often the daily message runs (supports times like `30s`, `5m`, `2h`, `1d`, `2h30m`, `1d4h20m10s`) (admin only).

**/daily_channel [mode] [channel]**  
Configure which channel daily messages use: “random” channel or a fixed specified channel (admin only).

**/daily_uniqueness [threshold]**  
Set how unique daily messages should be (from 0.0 to 1.0, where higher is stricter, default = 0.6) (admin only).

**/daily_prompt [prompt]**  
Set a custom daily prompt that overrides the default outrageous message prompt (admin only).

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

## Development notes

- Add new slash commands by creating modules in the `commands/` directory.
- `ai.py` contains the integration with the language model, adjust prompt templates and parameters there.
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

## License

MIT License – See LICENSE file for details.
