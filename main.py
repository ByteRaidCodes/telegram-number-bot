import os
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

API_URL = "https://adhartofamily.vercel.app/fetch?key=kalyug_here&aadhaar=222222222222"

def format_response(data):
    message = "📡 *Family Details*\n\n"
    
    message += f"🆔 *RC ID:* `{data.get('rcId', '-')}`\n"
    message += f"🏡 *Scheme:* {data.get('schemeName', '-')} ({data.get('schemeId', '-')})\n\n"

    members = data.get("memberDetailsList", [])
    message += "👨‍👩‍👧 *Family Members:*\n"
    
    for i, m in enumerate(members, start=1):
        uid = "✔️" if m.get("uid") == "Yes" else "❌"
        name = m.get("memberName", "Unknown").strip().title()
        relation = m.get("releationship_name", "-").title()
        message += f"{i}. {name} — {relation} — UID: {uid}\n"

    message += f"\n📍 District: {data.get('homeDistName', '-')}\n"
    message += f"🗺️ State: {data.get('homeStateName', '-')}\n"
    message += f"📌 Allowed OnOrc: {data.get('allowed_onorc', '-')}\n"

    return message

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is Live! Use /true to get details 📡")

async def true_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get(API_URL, timeout=10)
        data = response.json()

        formatted = format_response(data)

        await update.message.reply_text(formatted, parse_mode="Markdown")

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
