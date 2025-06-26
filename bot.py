import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv('7777811993:AAEXpM7n8-9hjIe17ETvWK03hOKrvEX0USg')
WEB_URL = os.getenv('WEB_URL')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📤 Send me any file (up to 4GB) and I'll generate a 24-hour download link!\n"
        "⚠️ Files auto-delete after 24 hours"
    )

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        message = update.message
        file = (message.document or message.video or message.audio)
        
        if not file:
            await message.reply_text("Please send a document, video, or audio file.")
            return

        file_obj = await file.get_file()
        filename = file.file_name or f"file_{file.file_id[:8]}{os.path.splitext(file.file_name or '')[1]}"
        download_path = f"uploads/{filename}"
        
        await file_obj.download_to_drive(download_path)
        await message.reply_text(
            f"🔗 Your 24-hour download link:\n\n"
            f"{WEB_URL}/view/{filename}\n\n"
            "⚠️ Link expires in 24 hours"
        )
    except Exception as e:
        logging.error(f"Error: {e}")
        await message.reply_text("❌ Error processing file. Please try again.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(
        filters.Document.ALL | filters.VIDEO | filters.AUDIO,
        handle_file
    ))
    app.run_polling()

if __name__ == '__main__':
    main()