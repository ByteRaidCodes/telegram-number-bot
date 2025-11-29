import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

API_BASE = "https://adhartofamily.vercel.app/fetch"
API_KEY = "kalyug_here"


def format_family(data):
    msg = "🏛 *Ration Card Details*\n\n"

    msg += f"🆔 *RC ID:* `{data.get('rcId','-')}`\n"
    msg += f"🏷 *Scheme:* {data.get('schemeName','-')} ({data.get('schemeId','-')})\n\n"

    msg += "👨‍👩‍👧 *Family Members:*\n"

    for i, m in enumerate(data.get("memberDetailsList", []), start=1):
        name = m.get("memberName", "-").strip().title()
        rel = m.get("releationship_name", "-").title()
        uid = "✔️" if m.get("uid") == "Yes" else "❌"
        msg += f"{i}. {name} — {rel} — UID: {uid}\n"

    msg += "\n📍 District: " + data.get("homeDistName", "-").title()
    msg += "\n🗺️ State: " + data.get("homeStateName", "-").title()
    msg += "\n⭕ Allowed OnOrc: " + data.get("allowed_onorc", "-")

    return msg


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bot is live! Use /true <aadhaar_number> to fetch data 📡"
    )


async def true_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text(
            "⚠️ Please enter Aadhaar number. Example: /true 222222222222"
        )
        return

    aadhaar = args[0]
    params = {"key": API_KEY, "aadhaar": aadhaar}

    try:
        resp = requests.get(API_BASE, params=params, timeout=10)
        data = resp.json()
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")
        return

    formatted = format_family(data)
    await update.message.reply_text(formatted, parse_mode="Markdown")


def main():
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN missing! Add it to Railway settings.")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("true", true_cmd))
    app.run_polling()


if __name__ == "__main__":
    main()

