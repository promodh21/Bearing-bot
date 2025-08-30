# ==============================
# Bearings Enquiry Bot
# ==============================

import pandas as pd
from rapidfuzz import process, fuzz
import re, nest_asyncio, asyncio, os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler, ContextTypes

# 🔑 Bot Token from Replit Secret
BOT_TOKEN = os.getenv("8116956908:AAHPwKQ4tZi7m0zaeYbcHpu0V_KMXpd5oNQ")

# ==============================
# Sample Bearings Database
# ==============================
rows = [
    ["6205 ZZ C3", "Deep groove ball bearing", "6205", "25x52x15", "Generic", "Also SKF/NSK/FAG equivalents"],
    ["22211EAB33", "Spherical roller bearing", "22211E", "55x100x25", "NRB", ""],
    ["NU205", "Cylindrical roller bearing (NU)", "NU205", "25x52x15", "Generic", ""],
    ["LMF20LUU", "Linear bushing (flange, long)", "LMF20", "20x32x45", "THK", ""],
    ["MGN9C", "Linear guide block", "MGN9", "Rail size 9", "HIWIN", "Carriage type C"],
    ["HR32004XJ", "Tapered roller bearing", "HR32004", "20x42x15", "NSK", ""],
    ["R1438HH", "Miniature ball bearing", "R1438", "3.175x9.525x3.967", "NMB", ""],
]
DB = pd.DataFrame(rows, columns=["part_number","type","series","size","brand","notes"])
DB["_key"] = DB["part_number"].str.upper()

# ==============================
# Helper functions
# ==============================
def normalize(text): 
    return re.sub(r"[\\s\\-\\_/]+"," ", text.upper()).strip()

def search_db(query, limit=5):
    q = normalize(query)
    matches = process.extract(q, DB["_key"].tolist(), scorer=fuzz.WRatio, limit=limit)
    out = []
    for m in matches:
        idx = m[2]
        row = DB.iloc[idx].to_dict()
        row["_score"] = int(m[1])
        out.append(row)
    return out

def format_row(row):
    return (f"*Part*: `{row['part_number']}`\\n"
            f"*Type*: {row['type']}\\n"
            f"*Series*: {row['series']}\\n"
            f"*Size*: {row['size']}\\n"
            f"*Brand*: {row['brand']}\\n"
            f"*Notes*: {row['notes']}\\n"
            f"*Match*: {row['_score']}%")

# ==============================
# Handlers
# ==============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Bearings Bot ready!\\nSend me a part number like `6205 ZZ C3`, `NU205`, or `LMF20LUU`.",
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.message.text or ""
    results = search_db(q)
    if results:
        text = "\\n\\n".join([format_row(r) for r in results])
    else:
        text = "❌ No match found. Add it to DB later."
    await update.message.reply_text(text, parse_mode="Markdown")

# ==============================
# Run bot
# ==============================
nest_asyncio.apply()

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is running... keep this terminal open!")
    await app.run_polling()

asyncio.run(main())
