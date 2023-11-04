import telebot
from telebot import types
import time
import requests
import json


welcome_message = """
🤖 Welcome to the Jasmin Bot! 🤖

I'm here to assist you with a wide range of tasks using the power of artificial intelligence. 🚀

You can ask me questions, get recommendations, translate languages, and more. Just type your query, and I'll do my best to provide you with a helpful response.

Here are some things you can try:
- "Tell me a joke 🤣"
- "Translate 'hello' to French 🇫🇷"
- "Give me a fun fact 🧠"
- "What's the weather like in New York? ☀️"

Feel free to explore and discover what I can do. If you ever need assistance, just type "/ask."

Let's get started! 🎉
"""

bot_token = '6965020592:AAEFbmzi1SPWGKGNVx1efKk_7AsDcvvlJmg'
bot = telebot.TeleBot(bot_token)
bot_start_time = time.time()
chat_history = {}


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    chat_history[user_id] = []
    markup = telebot.types.InlineKeyboardMarkup()
    buttons = [
        ("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀᴛ", "https://t.me/Jas_X_Bot?startgroup=true"),
        ("🗣️ ꜱᴜᴘᴘᴏʀᴛ", "https://t.me/+fYQTUBEvlb1iYTA9"),
        ("📣 ᴜᴘᴅᴀᴛᴇꜱ", "https://t.me/Toxic_TV_24"),
    ]
    for button_text, url in buttons:
        button = telebot.types.InlineKeyboardButton(button_text, url=url)
        markup.add(button)
        photo_url = 'https://telegra.ph/file/484aae5d970d9666b805a.jpg'
        bot.send_photo(message.chat.id, photo=photo_url, caption=welcome_message, reply_markup=markup)
        
        
        
@bot.message_handler(commands=['ping','alive'])
def ping(message):
    start_time = time.time()
    end_time = time.time()
    ping_time = round((end_time - start_time) * 1000, 2)
    current_time = time.time()
    uptime_seconds = current_time - bot_start_time
    uptime_minutes = int(uptime_seconds / 60)
    uptime_hours = int(uptime_minutes / 60)
    uptime_days = int(uptime_hours / 24)
    uptime_message = f"{uptime_days} days, {uptime_hours % 24} hours, {uptime_minutes % 60} minutes"
    caption = f"╰☞ 𝗣𝗢𝗡𝗚™╮\n☞ {ping_time} ms\n☞ {uptime_message}"
    photo_url = 'https://telegra.ph/file/484aae5d970d9666b805a.jpg'
    markup = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton("⚜ Cԋαɳɳҽʅ ⚜", url="https://t.me/toxic_tv_24")
    markup.add(url_button)
    bot.send_photo(message.chat.id, photo=photo_url, caption=caption, reply_markup=markup)
    
    
    
    
    
    
@bot.message_handler(commands=['ask'])
def ask(message):
    user_id = message.chat.id
    chat_history[user_id] = []  # Reset chat history for the user
    bot.reply_to(message, "Sure, please ask your question, and I'll do my best to answer!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    user_question = message.text

    if user_id in chat_history:
        chat_history[user_id].append(user_question)

        # Continue with the normal response
        api_url = f'https://chatgpt.apinepdev.workers.dev/?question={user_question}'
        response = fetch_api_response(api_url)
        cutom_print = response + "\n\nJOIN: @Toxic_TV_24"
        arturo = "SomeAsked: " + user_question

        bot.reply_to(message, cutom_print)
        print(arturo)
    else:
        bot.reply_to(message, "Please start the conversation with:\n/start to start bot\n/ask to ask questions.")

def fetch_api_response(api_url):
    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            api_response = json.loads(response.text)
            answer = api_response.get('answer', 'I am sorry, I cannot answer your question at the moment. Please ask another question.')
            response_with_emoji = "  " + answer
            return response_with_emoji
        else:
            return "Sorry, I couldn't fetch a response at the moment. Please try again later."
    except Exception as e:
        print("Error fetching API response:", str(e))
        return "An error occurred while fetching the response. Please try again later."


 
print("Bot Started....")
bot.polling()
