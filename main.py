from dotenv import load_dotenv
load_dotenv()

import os
import nest_asyncio
import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# Важливо!
nest_asyncio.apply()

# Токени з оточення
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Налаштування Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# Інструкції
SYSTEM_INSTRUCTIONS = """
You are a telegram bot, a friendly fitness coach for complete beginners.
Always be encouraging and supportive.
Suggest simple at-home workouts that don’t require equipment.
Avoid strict diets or intense routines.
Speak in simple terms and never shame the user.
If a user says they’re tired, cheer them up and remind them progress takes time.
"""

# Обробка /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi there! I’m your friendly fitness buddy. Ready to start your journey with some simple and fun workouts? Just ask me anything — I’m here to help!")

# Інструкції /instructions
async def instructions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(SYSTEM_INSTRUCTIONS)

# Повідомлення
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        chat = model.start_chat(history=[])
        response = chat.send_message(f"{SYSTEM_INSTRUCTIONS}\n\nUser query: {user_message}")
        reply = response.text
    except Exception as e:
        reply = f"Error: {str(e)}"
    await update.message.reply_text(reply)

# Обробка помилок
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Error: {context.error}")

# Запуск
if __name__ == "__main__":
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("instructions", instructions))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error)
    print("Bot is running…")
    application.run_polling()
