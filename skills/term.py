import os
import subprocess
from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler
from .utils import has_access
from functools import partial


COMMAND = 0

@has_access
def term(bot, update, conf):
    cwd = os.getcwd()
    update.message.reply_text('Terminal Mode:\n Bionic_Phoenix$ ')
    return COMMAND

@has_access
def command(bot, update, conf):
    command = update.message.text
    cwd = os.getcwd()
    stdout = subprocess.getoutput(command)
    update.message.reply_text("Bionic_Phoenix$ " + command + '\n' + stdout)
    return COMMAND

@has_access
def exit(bot, update, conf):
    update.message.reply_text('Exit Terminal Mode...')
    return ConversationHandler.END

def term_handler(conf):
    handler = ConversationHandler(
            entry_points=[CommandHandler('term', partial(term, conf=conf))],
            states={
                COMMAND: [MessageHandler(Filters.text, partial(command, conf=conf))]
            },
            fallbacks=[CommandHandler('exit', partial(exit, conf=conf))]
    )
    return handler
