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
        resp = requests.get(url).json()
        await update.message.reply_text(f"📱Data:\n{json.dumps(resp, indent=2)}")
    except:
        await update.message.reply_text("⚠️ Error")

async def get_true2_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Usage: /true2 222222222222")

    aadhaar = context.args[0]
    url = f"https://adhartofamily.vercel.app/fetch?key=kalyug_here&aadhaar={aadhaar}"
    try:
        resp = requests.get(url).json()

        # Extract JUST THE KEYS
        keys = list(resp.keys())

        formatted = "\n".join([f"• {k}" for k in keys])

        await update.message.reply_text(
            f"📌 API Field Names:\n\n{formatted}"
        )

    except Exception as e:
        await update.message.reply_text("⚠️ API Error")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n"
        "/true <number>\n"
        "/true2 <aadhaar> (keys only)"
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("true", get_true_info))
    app.add_handler(CommandHandler("true2", get_true2_info))
    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
