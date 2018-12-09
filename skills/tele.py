"""
    This skill is a bit different than the others
    as it might not be triggered by the user input
"""
from .utils import has_access
from telegram.ext import CommandHandler
from functools import partial

def get_status(bot, update):
    #if has_access(update, conf):
    update.message.reply_text("Get_status")

def tele_handler(conf):
    # p = subprocess.Popen(["python", "./bionic_phoenix_service.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # out, err = p.communicate()
    # result = p.returncode
    # p = Process(target=make_tele, args=(conf))
    # p.start()
    # p.join()
    #tele = Tele(conf)
    #b.start_service()
    #tele = Tele(conf)


    handler = CommandHandler("tele", get_status)
    return handler
