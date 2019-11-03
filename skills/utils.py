import sys
import traceback
from functools import wraps
from telegram.ext import ConversationHandler

WORD_LIMIT = 4096

def has_access(func):
    """
        this function checks whether user has access
    """
    @wraps(func)
    def _wrapper(update, context, conf, *args, **kwargs):
        try:
            user = update.message.from_user
            id = int(user['id'])
            if id in conf["white_list"]:
                return func(update, context, conf, *args, **kwargs)
            update.message.reply_text("You don't have access to me yet.")
        except Exception as e:
            et, ei, tb = sys.exc_info()
            stack = traceback.extract_tb(tb)
            (filename, line, procname, text) = stack[-1]
            update.message.reply_text('Error occurs in ' + procname + ': ' + type(e).__name__ + ": " + str(e))
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
