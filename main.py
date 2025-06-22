import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "7241333538:AAHGxIFsymBz46-vIv_hmfsz4GAXeRjdsg0"

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Welcome to Filmyzilla Movie Finder Bot!\nSend any movie name to get direct download links.\n\n👨‍💻 Made by Ritik Yadav"
    )

def search_filmyzilla(movie_name):
    query = f"site:filmyzilla.re {movie_name} full movie download"
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    links = []
    for g in soup.find_all('a'):
        href = g.get('href')
        if href and "/url?q=" in href and "webcache" not in href:
            actual_url = href.split("/url?q=")[1].split("&")[0]
            if "filmyzilla" in actual_url:
                links.append(actual_url)
        if len(links) >= 3:
            break

    return links

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie = update.message.text.strip()
    links = search_filmyzilla(movie)

    if not links:
        await update.message.reply_text("❌ No links found. Try a different movie name.")
        return

    reply = f"🎬 *Results for:* `{movie}`\n\n"
    for i, link in enumerate(links, 1):
        reply += f"{i}. [Link {i}]({link})\n"

    reply += "\n👨‍💻 *Made by Ritik Yadav*"
    await update.message.reply_markdown(reply)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.run_polling()

if __name__ == "__main__":
    main()
