from urllib import request
import simplejson as json
from .utils import has_access
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler
from functools import partial

SONG = 0

def lyrics(bot, update, args, conf):
    """
        Use Genius API to find songs according to input
        Currently using pre-generated access token
        More than willing to switch to OAuth2 once figure out how
    """
    if has_access(update, conf):
        if len(args) == 0:
            update.message.reply_text('/lyrics takes at least 1 argument')
            return ConversationHandler.END
        url = 'https://api.genius.com/search?q=' + '%20'.join(args) + '&access_token=' + conf['genius']['access_token']
        try:
            response = json.loads(request.urlopen(url).read())
            if response['meta']['status'] == 200:
                hits = response['response']['hits']
                reply_keyboard = [[song['result']['full_title']] for song in hits]
                update.message.reply_text(
                    'Select the song you want.',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
                )
                return SONG
            else:
                 update.message.reply_text("Failed to request Genius API")
                 return ConversationHandler.END
        except Exception as e:
            update.message.reply_text("Something went wrong when requesting Genius API: " + str(e))
            return ConversationHandler.END
    return ConversationHandler.END

def song(bot, update, conf):
    if has_access(update, conf):
        pass
    return ConversationHandler.END

def exit(bot, update, conf):
    if has_access(update, conf):
        update.message.reply_text('Exit Lyrics Mode...', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def lyrics_handler(conf):
    handler = ConversationHandler(
            entry_points=[CommandHandler('lyrics', partial(lyrics, conf=conf), pass_args=True)],
            states={
                SONG: [MessageHandler(Filters.text, partial(song, conf=conf))]
            },
            fallbacks=[CommandHandler('exit', partial(exit, conf=conf))]
    )
    return handler
