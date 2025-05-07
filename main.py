import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from fastapi import FastAPI

# اطلاعات محیطی
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# FastAPI app
fastapi_app = FastAPI()

@fastapi_app.get("/")
async def root():
    return {"status": "🟢 DarkYar bot is alive and running!"}

# تعریف هندلر ربات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من دارک‌یارم 😈")

# اتصال FastAPI و ربات تلگرام
application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))

# اتصال FastAPI به webhook ربات
webhook_path = f"/webhook/{TOKEN}"
telegram_app = application.get_webhook_application(
    webhook_path=webhook_path,
    web_app=fastapi_app,
)

# خروجی نهایی برای Render
app = telegram_app
