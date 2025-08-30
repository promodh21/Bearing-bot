import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("7817416149:AAGTxaGV7OtCxDNdWmXt255TK9hFKwVSEB4")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello 👋! Send me a bearing number to search.")

async def search_bearing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text(f"🔎 Searching info for bearing: {query}")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_bearing))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
