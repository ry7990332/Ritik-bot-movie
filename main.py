import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "7241333538:AAHGxIFsymBz46-vIv_hmfsz4GAXeRjdsg0"
PRMOVIE_URL = "https://prmovies.credit"

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Send any movie name to get Watch/Download link from PRMovies.\n\n👨‍💻 Made by Ritik Yadav"
    )

def search_prmovies(query):
    search_url = f"{PRMOVIE_URL}/?s={query.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    res = requests.get(search_url, headers=headers)

    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("h2", class_="title")

    links = []
    for r in results:
        a_tag = r.find("a")
        if a_tag:
            title = a_tag.text.strip()
            url = a_tag['href']
            if "/movie/" in url:  # Optional filter
                links.append((title, url))
        if len(links) >= 3:
            break

    return links

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    movies = search_prmovies(query)

    if not movies:
        await update.message.reply_text("❌ No results found. Try another movie name.")
        return

    reply = f"🎬 *Results for:* `{query}`\n\n"
    for name, link in movies:
        reply += f"🔗 [{name}]({link})\n"

    reply += "\n👨‍💻 *Made by Ritik Yadav*"
    await update.message.reply_markdown(reply)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
