from keep_alive import keep_alive
keep_alive()
import telebot
import gspread
from config import BOT_TOKEN, SHEET_ID, SHEET_NAME
from oauth2client.service_account import ServiceAccountCredentials
import os

bot = telebot.TeleBot(BOT_TOKEN)

sheet = None
try:
    # --- Google Sheet Setup ---
    if os.path.exists("service_account.json"):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)
        print("✅ Connected to Google Sheet successfully.")
    else:
        print("⚠️ Warning: service_account.json not found. Data won't be saved to Sheet.")
except Exception as e:
    print(f"⚠️ Google Sheet setup error: {e}")
    sheet = None

# --- Telegram Bot Handlers ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 नमस्कार Swapnil! मी तुझा Shiv Bot आहे — सुरू आहे आणि मेसेज घेतोय 📩")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    text = message.text
    user = message.from_user.first_name
    chat_id = message.chat.id

    if sheet:
        try:
            sheet.append_row([str(chat_id), user, text])
            bot.reply_to(message, f"📊 तुझा मेसेज Sheet मध्ये सेव्ह झाला आहे, {user} ✅")
        except Exception as e:
            bot.reply_to(message, f"⚠️ Sheet सेव्ह करताना त्रुटी: {e}")
    else:
        bot.reply_to(message, f"📩 {user}, तुझा मेसेज मिळाला! (Sheet शी कनेक्शन नाही).")

print("🤖 Bot is running... (no crash mode)")
bot.polling(non_stop=True)
