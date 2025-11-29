import os
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Set in Railway

# Your API URL fixed here
API_URL = "https://adhartofamily.vercel.app/fetch?key=kalyug_here&aadhaar=222222222222"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is Live! Use /true to get data 📡")

async def true_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get(API_URL, timeout=10)

        try:
            result = response.json()
        except:
            result = response.text

        await update.message.reply_text(f"📡 API Response:\n{result}")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

def main():
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN missing! Set it in Railway.")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("true", true_cmd))

    app.run_polling()

if __name__ == "__main__":
    main()
