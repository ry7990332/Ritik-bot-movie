import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "7241333538:AAHGxIFsymBz46-vIv_hmfsz4GAXeRjdsg0"
PRMOVIE_BASE = "https://prmovies.credit"

logging.basicConfig(level=logging.INFO)

def format_movie_url(name):
    name = name.lower().replace(" ", "-")
    return f"{PRMOVIE_BASE}/{name}-Watch-online-full-movie/"

def check_url_exists(url):
    try:
        res = requests.head(url, allow_redirects=True, timeout=5)
        return res.status_code == 200
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Send any movie name. I'll find the PRMovies link.\n\n👨‍💻 Made by Ritik Yadav")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    movie_url = format_movie_url(query)

    if check_url_exists(movie_url):
        reply = f"🎬 *{query.title()}*\n\n🔗 [Watch / Download Here]({movie_url})\n\n👨‍💻 *Made by Ritik Yadav*"
        await update.message.reply_markdown(reply)
    else:
        await update.message.reply_text("❌ Movie not found on PRMovies. Check spelling or try a different title.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.run_polling()

if __name__ == "__main__":
    main()
