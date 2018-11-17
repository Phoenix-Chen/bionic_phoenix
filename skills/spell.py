from .utils import has_access
from telegram.ext import CommandHandler
from functools import partial
import simplejson as json
from urllib import request

def spell(bot, update, args, conf):
    """
        Use Spellcheck API: https://market.mashape.com/montanaflynn/spellcheck
    """
    if has_access(update, conf):
        if len(args) == 0:
            update.message.reply_text('/spell takes at least 1 argument')
        else:
            headers={
                "X-Mashape-Key": conf['spellcheck'],
                "Accept": "application/json"
            }
            url = 'https://montanaflynn-spellcheck.p.mashape.com/check/?text=' + '+'.join(args)
            req = request.Request(url, headers=headers)
            response = json.loads(request.urlopen(req).read())
            # Recommand top 10 if input is single word
            # Recommand correction if input is not single word
            if len(args) == 1:
                update.message.reply_text('\n'.join(response['corrections'][response['original']][:10]))
            else:
                update.message.reply_text(response["suggestion"])

def spell_handler(conf):
    handler = CommandHandler("spell", partial(spell, conf=conf), pass_args=True)
    return handler
