import os

from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

SECRET_KEY = os.environ.get('SECRET_KEY')


class BotAPI:
    updater = Updater(SECRET_KEY, use_context=True)

    def __init__(self):
        self.updater.dispatcher.add_handler(
            CommandHandler('start', self.start))
        self.updater.dispatcher.add_handler(
            CommandHandler('youtube', self.youtube_url))
        self.updater.dispatcher.add_handler(CommandHandler('help', self.help))
        self.updater.dispatcher.add_handler(
            CommandHandler('linkedin', self.linkedIn_url))
        self.updater.dispatcher.add_handler(
            CommandHandler('gmail', self.gmail_url))
        self.updater.dispatcher.add_handler(
            CommandHandler('geeks', self.geeks_url))
        self.updater.dispatcher.add_handler(
            MessageHandler(Filters.text, self.unknown))
        self.updater.dispatcher.add_handler(
            MessageHandler(Filters.command, self.unknown))
        self.updater.dispatcher.add_handler(
            MessageHandler(Filters.text, self.unknown_text))

    def start(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            "Hello, Welcome to my bot.")

    def help(self, update: Update, context: CallbackContext):
        update.message.reply_text("Help message")

    def gmail_url(self, update: Update, context: CallbackContext):
        update.message.reply_text("gmail link here")

    def youtube_url(self, update: Update, context: CallbackContext):
        update.message.reply_text("youtube link")

    def linkedIn_url(self, update: Update, context: CallbackContext):
        update.message.reply_text("Your linkedin profile url")

    def geeks_url(self, update: Update, context: CallbackContext):
        update.message.reply_text("GeeksforGeeks url here")

    def unknown_text(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            "Sorry I can't recognize you , you said '%s'" % update.message.text)

    def unknown(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            "Sorry '%s' is not a valid command" % update.message.text)
