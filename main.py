from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler, ContextTypes
import json
import os
from config import BOT_TOKEN, DATA_FILE
from responses import generate_response, update_user_score

# ایجاد فایل دیتا در صورت عدم وجود
if not os.path.exists("data"):
    os.makedirs("data")
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

# فرمان شروع
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من دارک‌یارم، یارِ تحلیل‌گر شما با لهجه‌ی کرمانی!")

# پاسخ به پیام‌ها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    text = update.message.text
    response, user_data = generate_response(user_id, text)
    update_user_score(user_id, user_data)
    await update.message.reply_text(response)

# اجرای ربات
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    app.run_polling()