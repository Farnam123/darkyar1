import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.ext.webhookhandler import WebhookRequestHandler
from fastapi import FastAPI, Request
import telegram

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.environ.get("PORT", 8080))

app = FastAPI()
bot_app = Application.builder().token(TOKEN).build()

# فرمان start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من دارک‌یارم 😈")

bot_app.add_handler(CommandHandler("start", start))

# هندل کردن webhook با FastAPI
@app.post(f"/webhook/{TOKEN}")
async def webhook(request: Request):
    data = await request.body()
    await bot_app.update_queue.put(telegram.Update.de_json(data.decode(), bot_app.bot))
    return {"status": "received"}

@app.get("/")
async def root():
    return {"status": "🟢 DarkYar bot is alive and running!"}

# راه‌اندازی Webhook
if __name__ == "__main__":
    import uvicorn

    async def set_webhook():
        await bot_app.bot.set_webhook(f"{WEBHOOK_URL}/webhook/{TOKEN}")

    bot_app.initialize()
    bot_app.post_init(set_webhook)
    uvicorn.run(app, host="0.0.0.0", port=PORT)
