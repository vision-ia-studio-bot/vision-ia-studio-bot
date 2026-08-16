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
from stats import add_user, get_user_count

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
    add_user(update.effective_user.id)

    await update.message.reply_text(
        "🤖 Bonjour ! Je suis Vis Assistant."
    )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.message.reply_text(
        "🤖 Vis Assistant\n\n"
        "Commandes disponibles :\n\n"
        "/start - Démarrer le bot\n"
        "/help - Afficher cette aide\n"
        "/stats - Voir le nombre d'utilisateurs\n"
        "/web - Rechercher sur Internet\n\n"
        "📄 Envoyez un PDF pour obtenir un résumé.\n"
        "💬 Envoyez un message pour discuter avec l'IA."
    )


async def stats_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.message.reply_text(
        f"👥 Nombre d'utilisateurs : {get_user_count()}"
    )


async def web_search(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
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

    if not document.file_name.lower().endswith(".pdf"):
        return

    await update.message.reply_text(
        "📄 PDF reçu. Analyse en cours..."
    )

    telegram_file = await document.get_file()

    pdf_path = f"/tmp/{document.file_name}"

    await telegram_file.download_to_drive(pdf_path)

    text = extract_text(pdf_path)

    if not text:
        await update.message.reply_text(
            "Impossible de lire ce document."
        )
        return

    summary = ask_ai(
        f"Résume ce document :\n\n{text[:5000]}"
    )

    await update.message.reply_text(summary)


async def reply(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user_id = update.effective_user.id
    message = update.message.text

    add_user(user_id)

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
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stats", stats_command))
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
