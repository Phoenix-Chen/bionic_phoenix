from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler
from .utils import has_access
from functools import partial

def conversation(bot, update, conf):
    if has_access(update, conf):
        update.message.reply_text("NLP skill not deployed...")

def conversation_handler(conf):
    handler = MessageHandler(Filters.text, partial(conversation, conf=conf))
    return handler
