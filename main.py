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

        # PRINT FULL RAW JSON TO CONSOLE / LOGS
        print("\n===== RAW API DATA =====")
        print(json.dumps(response, indent=2))
        print("========================\n")

        await update.message.reply_text("🧪 Testing complete!\nCheck Railway Logs for full data.")

    except Exception as e:
        print("API ERROR:", e)
        await update.message.reply_text("⚠️ API Error — Try later!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send `/num 6200303551` to test!")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("num", get_number_info))

    print("Bot running…")
    app.run_polling()

if __name__ == "__main__":
    main()
