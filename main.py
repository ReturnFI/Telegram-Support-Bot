import telebot
from dotenv import load_dotenv
import os

load_dotenv()
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(telegram_token)
user_messages = {}

@bot.message_handler(commands=['start'])
def start(message):
    try:
        command_value = message.text.split(' ', 1)[1].strip()
        group_chat_id, thread_id = map(int, command_value.split('_'))
        handle_start_command(message, group_chat_id, thread_id)
    except (IndexError, ValueError):
        bot.reply_to(message, "Invalid command format.")

def handle_start_command(message, group_chat_id, thread_id):
    user_messages[message.chat.id] = {
        'group_id': group_chat_id,
        'thread_id': thread_id,
        'username': message.from_user.username,
        'group_message_id': None
    }
    bot.send_message(message.chat.id, f"You have selected thread ID '{thread_id}'. Please send your message or photo with caption to the bot.")

@bot.message_handler(content_types=['photo', 'text'], func=lambda message: message.chat.type == 'private' and message.chat.id in user_messages)
def handle_message(message):
    try:
        user_data = user_messages[message.chat.id]
        group_id = user_data['group_id']
        thread_id = user_data['thread_id']
    
        if message.photo:
            photo = message.photo[-1]
            caption = message.caption if message.caption else "No caption provided."
    
            forwarded_message = bot.send_photo(
                group_id,
                photo.file_id,
                caption=f"Thread ID: {thread_id}\n\n@{message.from_user.username} (ID: {message.chat.id}):\n{caption}",
                reply_to_message_id=thread_id
            )
            user_messages[message.chat.id]['group_message_id'] = forwarded_message.message_id
            bot.send_message(message.chat.id, f"Your photo with caption for thread ID '{thread_id}' has been sent. Please wait for Hiddify Team's response.")
    
        elif message.text:
            if user_data['group_message_id'] is None:
                forwarded_message = bot.send_message(
                    group_id,
                    f"Thread ID: {thread_id}\n\n@{message.from_user.username} (ID: {message.chat.id}):\n\n{message.text}",
                    reply_to_message_id=thread_id
                )
                user_messages[message.chat.id]['group_message_id'] = forwarded_message.message_id
                bot.send_message(message.chat.id, f"Your message for thread ID '{thread_id}' has been sent. Please wait for Hiddify Team's response.")
            
            else:
                forwarded_message = bot.send_message(
                    group_id,
                    f"Thread ID: {thread_id}\n\n@{message.from_user.username} (ID: {message.chat.id}) replied:\n\n{message.text}",
                    reply_to_message_id=user_data['group_message_id']
                )
                user_messages[message.chat.id]['group_message_id'] = forwarded_message.message_id
    
    except telebot.apihelper.ApiException as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}. Please try again later.")

@bot.message_handler(commands=['join'], func=lambda message: message.chat.type == 'supergroup')
def join(message):
    try:
        group_id = message.chat.id
        bot_username = bot.get_me().username
        
        if message.is_topic_message:
            thread_id = message.message_thread_id
            join_url = f"tg://resolve?domain={bot_username}&start={group_id}_{thread_id}"
            bot.send_message(message.chat.id, f"Use the following link to join this group and topic:\n\n{join_url}", message_thread_id=thread_id)
        else:
            bot.send_message(message.chat.id, "This command should be used within a thread in the group to create a join link for that specific thread.")
    
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}. Please try again later.")

@bot.message_handler(func=lambda message: (
    message.chat.type == 'supergroup' and 
    message.reply_to_message is not None and 
    message.reply_to_message.from_user.id == bot.get_me().id and 
    message.text.startswith('/welcome ')
))
def handle_group_reply(message):
    try:
        replied_message_id = message.reply_to_message.message_id
        for user_id, user_data in user_messages.items():
            if user_data.get('group_message_id') == replied_message_id:
                reply_text = message.text.split('/welcome ', 1)[1]
                bot.send_message(user_id, f"Hiddify Team:\n\n{reply_text}")
                break
    
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}. Please try again later.")

bot.polling()
