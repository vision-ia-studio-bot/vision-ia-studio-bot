import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = """
🤖 Bienvenue sur Vis Assistant.

Commandes disponibles :

/aide
/traduire <texte>
/resumer <texte>

Vous pouvez également m'envoyer un message.
"""

    await update.message.reply_text(message)


async def aide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commandes :\n"
        "/traduire Bonjour le monde\n"
        "/resumer Collez votre texte après la commande."
    )


async def traduire(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texte = " ".join(context.args)

    if not texte:
        await update.message.reply_text(
            "Utilisation : /traduire Bonjour le monde"
        )
        return

    dictionnaire = {
        "bonjour": "hello",
        "merci": "thank you",
        "au revoir": "goodbye",
        "comment vas-tu": "how are you",
    }

    resultat = dictionnaire.get(
        texte.lower(),
        "Traduction indisponible pour le moment."
    )

    await update.message.reply_text(resultat)


async def resumer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texte = " ".join(context.args)

    if not texte:
        await update.message.reply_text(
            "Ajoutez un texte après /resumer."
        )
        return

    mots = texte.split()

    if len(mots) <= 40:
        resume = texte
    else:
        resume = " ".join(mots[:40]) + "..."

    await update.message.reply_text(f"Résumé :\n{resume}")


async def reponse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Vous avez écrit : {update.message.text}"
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("aide", aide))
    app.add_handler(CommandHandler("traduire", traduire))
    app.add_handler(CommandHandler("resumer", resumer))

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, reponse)
    )

    app.run_polling()


if __name__ == "__main__":
    main()
