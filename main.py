import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")  # your bot token from Railway / env

API_BASE = "https://adhartofamily.vercel.app/fetch"
API_KEY = "kalyug_here"  # as per your API

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bot is live! Use /true <aadhaar_number> to fetch data."
    )

async def true_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text(
            "⚠️ Please provide Aadhaar number. Example: /true 222222222222"
        )
        return

    aadhaar = args[0]

    params = {
        "key": API_KEY,
        "aadhaar": aadhaar
    }

    try:
        resp = requests.get(API_BASE, params=params, timeout=15)
        data = resp.json()
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")
        return

    # Send raw JSON response to you — good for testing
    await update.message.reply_text(f"📡 API Response:\n{data}")

def main():
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN not provided!")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("true", true_cmd))

    app.run_polling()

if __name__ == "__main__":
    main()
