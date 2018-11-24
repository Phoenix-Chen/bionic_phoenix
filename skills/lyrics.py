from urllib import request
import simplejson as json
from .utils import has_access
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import CommandHandler, ConversationHandler, CallbackQueryHandler
from functools import partial
from bs4 import BeautifulSoup

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
                reply_keyboard = [[InlineKeyboardButton(song['result']['full_title'], callback_data=str(song['result']['id']))] for song in hits]
                update.message.reply_text(
                    'Select the song you want.',
                    reply_markup=InlineKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
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
    query = update.callback_query
    song_id = query.data
    api_url = 'https://api.genius.com/songs/' + song_id + '?access_token=' + conf['genius']['access_token']
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}
    try:
        response = json.loads(request.urlopen(api_url).read())
        if response['meta']['status'] == 200:
            url = response['response']['song']['url']
            req = request.Request(url, headers=headers)
            soup = BeautifulSoup(request.urlopen(req).read(), 'html.parser')
            lyrics = soup.find("div", {"class" : "lyrics"}).text
            bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text=lyrics
            )
        else:
            bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text="Failed to request Genius API"
            )
    except Exception as e:
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text="Something went wrong when requesting Genius API: " + str(e)
        )
    return ConversationHandler.END

def exit(bot, update, conf):
    if has_access(update, conf):
        update.message.reply_text('Exit Lyrics Mode...')
    return ConversationHandler.END

def lyrics_handler(conf):
    handler = ConversationHandler(
            entry_points=[CommandHandler('lyrics', partial(lyrics, conf=conf), pass_args=True)],
            states={
                SONG: [CallbackQueryHandler(partial(song, conf=conf))]
            },
            fallbacks=[CommandHandler('exit', partial(exit, conf=conf))]
    )
    return handler
