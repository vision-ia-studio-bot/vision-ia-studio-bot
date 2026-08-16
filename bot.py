import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from ai import ask_ai
from memory import save_message, get_history
from internet import search_web
from pdf_reader import extract_text

BOT_TOKEN = os.getenv("BOT_TOKEN")

KEYWORDS = [
    "aujourd",
    "actualité",
    "actu",
    "récent",
    "dernière",
    "nouvelle",
    "coupe du monde",
    "gagné",
    "gagnant",
    "mois",
    "année",
    "date",
    "heure",
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bonjour ! Je suis Vis Assistant."
    )


async def web_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)

    if not query:
        await update.message.reply_text(
            "Utilisation : /web votre recherche"
        )
        return

    result = search_web(query)

    await update.message.reply_text(result)


async def handle_pdf(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    document = update.message.document

    if not document:
        return

    file = await document.get_file()

    pdf_path = f"/tmp/{document.file_name}"

    await file.download_to_drive(pdf_path)

    text = extract_text(pdf_path)

    if not text:
        await update.message.reply_text(
            "Impossible de lire ce document."
        )
        return

    summary = ask_ai(
        f"Résume le document suivant :\n\n{text[:5000]}"
    )

    await update.message.reply_text(summary)


async def reply(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user_id = update.effective_user.id
    message = update.message.text

    lower_message = message.lower()

    if any(word in lower_message for word in KEYWORDS):
        result = search_web(message)

        if result != "Aucun résultat trouvé.":
            await update.message.reply_text(result)
            return

    save_message(user_id, "user", message)

    history = get_history(user_id)

    context_text = "\n".join(
        f"{item['role']}: {item['content']}"
        for item in history
    )

    answer = ask_ai(context_text)

    save_message(user_id, "assistant", answer)

    await update.message.reply_text(answer)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("web", web_search))

    app.add_handler(
        MessageHandler(
            filters.Document.PDF,
            handle_pdf,
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            reply,
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()
