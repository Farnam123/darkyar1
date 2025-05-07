# main.py
import os
from fastapi import FastAPI, Request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = f"/{TOKEN}"
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}{WEBHOOK_PATH}"

app = FastAPI()
telegram_app = Application.builder().token(TOKEN).build()


# ⬇️ /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("📊 پروفایل من", callback_data="profile"),
            InlineKeyboardButton("🏆 رتبه‌بندی", callback_data="ranking"),
        ],
        [
            InlineKeyboardButton("⚙️ تنظیمات", callback_data="settings"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("سلام! خوش اومدی به دارک‌یار 🤖", reply_markup=reply_markup)


# ⬇️ پاسخ به دکمه‌های اینلاین
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "profile":
        await query.edit_message_text("📊 اینجا قراره پروفایل رفتاری شما نمایش داده بشه (در حال توسعه)")
    elif query.data == "ranking":
        await query.edit_message_text("🏆 لیست رتبه‌بندی کاربران گروه بزودی فعال میشه!")
    elif query.data == "settings":
        await query.edit_message_text("⚙️ بخش تنظیمات فعلاً در حال آماده‌سازیه.")


telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CallbackQueryHandler(button_handler))


# Webhook endpoint
@app.post(WEBHOOK_PATH)
async def telegram_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"status": "ok"}


@app.on_event("startup")
async def on_startup():
    await telegram_app.bot.set_webhook(url=WEBHOOK_URL)
    print(f"Webhook set to: {WEBHOOK_URL}")
