import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from fastapi import FastAPI
from starlette.requests import Request
import uvicorn

# اطلاعات لازم
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.environ.get("PORT", 8080))

# FastAPI app
fastapi_app = FastAPI()

@fastapi_app.get("/")
async def root():
    return {"status": "🟢 DarkYar bot is alive and running!"}

# ربات تلگرام
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من دارک‌یارم 😈")

# تابع اصلی اجرا
def main():
    app = ApplicationBuilder().token(TOKEN).get_webhook_application(
        webhook_path=f"/webhook/{TOKEN}",
        web_app=fastapi_app
    )

    app.add_handler(CommandHandler("start", start))

    # اجرای Webhook روی FastAPI
    uvicorn.run(
        fastapi_app,
        host="0.0.0.0",
        port=PORT
    )

if __name__ == '__main__':
    main()
