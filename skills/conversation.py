from telegram.ext import Filters, MessageHandler
from .utils import has_access
from functools import partial

@has_access
def conversation(bot, update, conf):
    update.message.reply_text("NLP skill not deployed...")

def conversation_handler(conf):
    handler = MessageHandler(Filters.text, partial(conversation, conf=conf))
    return handler
