import os
import yt_dlp
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

BOT_TOKEN = os.getenv("BOT_TOKEN")

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Send me a YouTube link to download.")

def download_video(update: Update, context: CallbackContext):
    url = update.message.text
    update.message.reply_text("Downloading...")

    ydl_opts = {'outtmpl': 'downloads/%(title)s.%(ext)s', 'format': 'best'}
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)
        
        update.message.reply_document(document=open(file_name, "rb"))

    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
