from os import path, mkdir
from telegram.ext import Filters, MessageHandler
from telegram import File
from .utils import has_access
from functools import partial

@has_access
def file(update, context, conf):
    file_id = update.message['document']['file_id']
    file_name = update.message['document']['file_name']
    new_file = context.bot.get_file(file_id)
    download_dir = conf['download_path']
    if not path.exists(download_dir):
        try:
            mkdir(download_dir)
        except OSError:
            print("Creation of the directory " + download_dir + " failed")
    exsist_name = 0
    while True:
        download_path = "{}/{}".format(download_dir, file_name)
        if not path.exists(download_path):
            new_file.download(download_path)
            update.message.reply_text(file_name + ' has been saved.')
            break
        exsist_name += 1
        file_name = update.message['document']['file_name']
        file_ext = file_name.split('.')[-1]
        file_name = file_name[:len(file_name) - len(file_ext) - 1] + '_' + str(exsist_name) + '.' + file_ext


def file_handler(conf):
    handler = MessageHandler(Filters.document, partial(file, conf=conf))
    return handler
