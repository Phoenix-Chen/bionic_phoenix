from telegram.ext import Filters, MessageHandler
from .utils import has_access
from functools import partial

@has_access
def convo(update, context, conf):
    update.message.reply_text("NLP skill not deployed...")

def convo_handler(conf):
    handler = MessageHandler(Filters.text, partial(convo, conf=conf))
    return handler
