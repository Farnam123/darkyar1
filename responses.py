import json
from config import DATA_FILE
import random

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def generate_response(user_id, message):
    data = load_data()
    user_data = data.get(user_id, {"score": 0, "messages": 0})

    message = message.lower()
    sentiment = "neutral"
    if "😡" in message or "لعنت" in message:
        sentiment = "negative"
        user_data["score"] -= 1
    elif "😂" in message or "عاشقتم" in message or "❤️" in message:
        sentiment = "positive"
        user_data["score"] += 1
    elif "خفه شو" in message:
        sentiment = "rude"
        user_data["score"] -= 2

    user_data["messages"] += 1

    data[user_id] = user_data
    response = random.choice([
        f"اِی جان! بازم پیام بده ببینم چه حالی داری 😎",
        f"خب که چی؟ نکنه می‌خوای زرنگ‌بازی دراری؟ 😂",
        f"امتیازت شده {user_data['score']} از {user_data['messages']} پیام. بد نیستا!",
        f"دارم نگات می‌کنم، مواظب حرف زدنت باش 😏",
        f"ها؟ همین بود حرفت؟ بیشتر از اینا ازت توقع داشتم!"
    ])
    return response, user_data

def update_user_score(user_id, user_data):
    data = load_data()
    data[user_id] = user_data
    save_data(data)