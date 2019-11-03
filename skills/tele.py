"""
    This skill is a bit different than the others
    as it might not be triggered by the user input
"""
from .utils import has_access, is_int
from telegram.ext import CommandHandler
from functools import partial
from service.utils import make_interface

@has_access
def get_status(update, context, conf):
    iface = make_interface()
    # If no argument passed show all current status
    if len(context.args) == 0:
        statuses = iface.get_processes()
        s = "PID\tSTART_TIME\tCOMMAND\tSTATUS\n" + "\n".join(statuses)
        update.message.reply_text(s)
    elif len(context.args) == 1 and context.args[0] == "--clean":
        statuses = iface.clean()
        s = "PID\tSTART_TIME\tCOMMAND\tSTATUS\n" + "\n".join(statuses)
        update.message.reply_text(s)
    elif len(context.args) == 2 and context.args[0] == "--kill":
        if is_int(context.args[1]):
            output = iface.terminate_process(int(context.args[1]))
            if output != '':
                update.message.reply_text(output)
        else:
            update.message.reply_text("PID must be integer.")


def tele_handler(conf):
    handler = CommandHandler("tele", partial(get_status, conf=conf))
    return handler
