# Telegram Support Bot
This is a Telegram bot designed to facilitate communication between users and a support team. The bot allows users to send messages or photos to a specific group thread, where the support team can respond.

## Features

- Users can start a support session by providing a group chat ID and thread ID.
- The bot forwards user messages and photos to the specified group thread.
- The support team can reply to user messages, and the bot forwards the responses back to the user.
- The bot can generate a join link for specific group threads.

## Requirements

- Python 3.6+
- `pyTelegramBotAPI` library
- `python-dotenv` library

## Installation
1. Clone the repository:
``` shell
git clone https://github.com/ReturnFI/Telegram-Support-Bot.git
cd telegram-support-bot
```

2. Install the required libraries:
```python
pip install pyTelegramBotAPI python-dotenv
```

3. Create a .env file in the root directory of the project and add your Telegram bot token:
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

## Usage
1. Start the bot:
```python
python main.py
```

## Commands
1. `/start <group_chat_id>_<thread_id>`
 - Starts a support session. The user needs to provide a valid `group_chat_id` and `thread_id`
2. `/join`
 - Used in a supergroup thread to generate a join link for that specific thread. The link can be shared with users to allow them to join the support session.
 - This command should be used within a thread in the group.

## Functionality

1. Handling user messages and photos:
- The bot will forward user messages and photos to the specified group thread.
- The forwarded message will include the user's username and ID for reference.
2. Handling replies from the support team:
- The support team can reply to the user's message by using the /welcome command followed by their message.
- Example: `/welcome Thank you for reaching out. How can we assist you today?`
- The bot will forward the support team's reply back to the user.

## Contributing
Feel free to open issues or submit pull requests if you find any bugs or have suggestions for improvements.
