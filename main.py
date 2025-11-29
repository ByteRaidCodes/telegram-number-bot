import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Token will come from Railway variable

async def get_number_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Send a number like: /num 6200303551")

    number = context.args[0]
    url = f"https://kalyug-papa.vercel.app/api/info?num={number}&key=papabolo"

    try:
        response = requests.get(url).json()
        if "error" in response:
            return await update.message.reply_text("❌ No data found or wrong number")

        text = (
            f"📞 *Phone Info:*\n"
            f"Number: {response.get('number', 'N/A')}\n"
            f"Owner: {response.get('name', 'N/A')}\n"
            f"State: {response.get('state', 'N/A')}\n"
            f"Carrier: {response.get('carrier', 'N/A')}\n"
        )
        await update.message.reply_text(text, parse_mode="Markdown")

    except:
        await update.message.reply_text("⚠️ API Error — Try later!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send `/num 6200303551` to get info!")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("num", get_number_info))

    print("Bot started…")
    app.run_polling()

if __name__ == "__main__":
    main()
