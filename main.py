import os
import json
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def get_true_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Usage: /true 9876543210")

    number = context.args[0]
    url = f"https://kalyug-papa.vercel.app/api/info?num={number}&key=papabolo"

    try:
        response = requests.get(url).json()

        if "error" in response:
            return await update.message.reply_text("❌ No info found")
            
    text = ""
        for key, value in safe_data.items():
            text += f"• {key.capitalize()}: {value}\n"

        if not text:
            text = "⚠️ No safe public information available"

        await update.message.reply_text(f"📱 Lookup Result:\n\n{text}")

    except Exception as e:
        await update.message.reply_text("⚠️ API Error — Try later!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use: /true 9876543210")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("true", get_true_info))

    print("Bot running…")
    app.run_polling()

if __name__ == "__main__":
    main()
