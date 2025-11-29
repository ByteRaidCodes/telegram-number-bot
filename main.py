import os
import json
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def get_number_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Send a number like: /num 6200303551")

    number = context.args[0]
    url = f"https://kalyug-papa.vercel.app/api/info?num={number}&key=papabolo"

    try:
        response = requests.get(url).json()
        print("\n📞 FULL NUMBER API DATA:\n", json.dumps(response, indent=2))
        await update.message.reply_text("📡 Number API Tested — check logs!")

    except Exception as e:
        await update.message.reply_text("⚠️ API Error (Number)")

async def get_aadhaar_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Send: /aadhaar 222222222222")

    aadhaar = context.args[0]
    url = f"https://adhartofamily.vercel.app/fetch?key=kalyug_here&aadhaar={aadhaar}"

    try:
        response = requests.get(url).json()
        print("\n🆔 FULL AADHAAR API DATA:\n", json.dumps(response, indent=2))
        await update.message.reply_text("🔐 Aadhaar Test Logged — check logs!")

    except Exception as e:
        await update.message.reply_text("⚠️ API Error (Aadhaar)")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n"
        "/num 6200303551 → Test Number API\n"
        "/aadhaar 222222222222 → Test Aadhaar API (logs only)"
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("num", get_number_info))
    app.add_handler(CommandHandler("aadhaar", get_aadhaar_info))

    print("Bot running…")
    app.run_polling()

if __name__ == "__main__":
    main()
