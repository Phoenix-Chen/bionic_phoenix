from functools import wraps
from telegram.ext import ConversationHandler

WORD_LIMIT = 4096

def has_access(func):
    """
        this function checks whether user has access
    """
    @wraps(func)
    def _wrapper(bot, update, conf, *args, **kwargs):
        try:
            user = update.message.from_user
            id = int(user['id'])
            if id in conf["white_list"]:
                return func(bot, update, conf=conf, *args, **kwargs)
            update.message.reply_text("You don't have access to me yet.")
        except Exception as e:
            update.message.reply_text("Error occur in has_access: " + str(e))
        return ConversationHandler.END
    return _wrapper


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_word(s):
    if s == '' or s == None:
        return False
    for c in s:
        if not c.isalpha():
            return False
    return True
