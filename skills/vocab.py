from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler
from .utils import has_access



@has_access
def vocab(bot, update, conf):
    pass

@has_access
def exit(bot, update, conf):
    update.message.reply_text('Exit Vocab Mode...')
    return ConversationHandler.END

def vocab_handler(conf):
    pass
