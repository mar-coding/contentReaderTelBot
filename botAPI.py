from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

import os

SECRET_KEY = os.environ.get('SECRET_KEY')

updater = Updater(SECRET_KEY, use_context=True)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello, Welcome to my bot.")


def help(update: Update, context: CallbackContext):
    update.message.reply_text("Help message")


def gmail_url(update: Update, context: CallbackContext):
    update.message.reply_text("gmail link here")


def youtube_url(update: Update, context: CallbackContext):
    update.message.reply_text("youtube link")


def linkedIn_url(update: Update, context: CallbackContext):
    update.message.reply_text("Your linkedin profile url")


def geeks_url(update: Update, context: CallbackContext):
    update.message.reply_text("GeeksforGeeks url here")


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text)


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('youtube', youtube_url))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('linkedin', linkedIn_url))
updater.dispatcher.add_handler(CommandHandler('gmail', gmail_url))
updater.dispatcher.add_handler(CommandHandler('geeks', geeks_url))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(
    # Filters out unknown commands
    Filters.command, unknown))

# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))


updater.start_polling()
