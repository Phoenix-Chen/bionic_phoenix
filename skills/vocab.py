from urllib import request
import simplejson as json
import emoji
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler, CallbackQueryHandler
from sqlalchemy.sql import exists
from .utils import has_access, is_word
from functools import partial

from database.utils import DBConnector
from database.models.vocab_schema import Vocabulary

_ENTRY_POINTS = 0
_DICT = 1
_ADD_CARD = 2
_GET_CARD = 3
_SHOW_DEF = 4
_ADD_CORRECT = 5

_last_search = None

class FlashCards:
    def __init__(self):
        self.db_connector = DBConnector('vocab')
        self.cards = None
        self.cur_ind = -1 # For convience
        self.reset_deck()

    def reset_deck(self):
        self.cards = self.db_connector.session.query(Vocabulary).order_by(Vocabulary.correct).all()
        self.cur_ind = -1

    def get_cur_word(self):
        if self.cur_ind == len(self.cards) - 1:
            self.reset_deck()
        return self.cards[self.cur_ind].word

    def next_card(self):
        self.cur_ind += 1

    def add_card(self):
        global _last_search
        if not self.db_connector.session.query(exists().where(Vocabulary.word == _last_search)).scalar():
            vocabulary = Vocabulary(word=_last_search)
            self.db_connector.session.add(vocabulary)
            self.db_connector.session.commit()

    def add_correct(self):
        vocabulary = self.cards[self.cur_ind]
        vocabulary.correct += 1
        self.db_connector.session.commit()

    def destory(self):
        self.db_connector.close()

_flash_cards = None

@has_access
def vocab(update, context, conf):
    global _flash_cards
    _flash_cards = FlashCards()
    reply_keyboard = [
        [InlineKeyboardButton('Dictionary', callback_data=_DICT)],
        [InlineKeyboardButton('Flash Card', callback_data=_GET_CARD)]
    ]
    update.message.reply_text(
        'What do you want to do?',
        reply_markup=InlineKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return _ENTRY_POINTS


def entry_points(update, context, conf):
    global _flash_cards
    query = update.callback_query
    option = int(query.data)
    if option == _DICT:
        context.bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text='Input the word you want to look up:'
        )
    elif option == _ADD_CARD:
        return add_card(context.bot, query)
    elif option == _GET_CARD:
        return get_card(context.bot, query)
    elif option == _SHOW_DEF:
        return show_def(context.bot, query, conf)
    elif option == _ADD_CORRECT:
        _flash_cards.add_correct()
        return get_card(context.bot, query)
    elif option == ConversationHandler.END:
        _flash_cards.destory()
        context.bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text='Exit Vocab Mode...'
        )
    return option


def merriam_webster(keyword, api_key) -> str:
    _RESULT_LIMIT = 4
    url = 'https://dictionaryapi.com/api/v3/references/collegiate/json/' + keyword + '?key=' + api_key
    result = ''
    try:
        response = json.loads(request.urlopen(url).read())[:_RESULT_LIMIT]
        for definition in response:
            if 'fl' in definition:
                result += definition['fl'] + '\n'
                for i in range(len(definition['shortdef'])):
                    result += str(i + 1) + ': ' + definition['shortdef'][i] + '\n'
            elif 'cxs' in definition:
                result += definition['cxs'][0]['cxl'] + ' ' + definition['cxs'][0]['cxtis'][0]['cxt'] + '\n'
            result += '\n'
    except Exception as e:
        print('Something went wrong when requesting Merriam Webster API: ' + str(e))
    return result


def dictionary(update, context, conf):
    word = update.message.text
    if not is_word(word):
        update.message.reply_text('Please input a valid word:')
        return _DICT
    result = merriam_webster(word, conf['merriam_webster'])
    global _last_search
    _last_search = word
    reply_keyboard = [
        [InlineKeyboardButton('See full definition', url='https://www.merriam-webster.com/dictionary/' + word)],
        [InlineKeyboardButton('Search new word', callback_data=_DICT)],
        [InlineKeyboardButton('Add to falsh cards', callback_data=_ADD_CARD)],
        [InlineKeyboardButton('Exit', callback_data=ConversationHandler.END)]
    ]
    update.message.reply_text(
        result,
        reply_markup=InlineKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return _ENTRY_POINTS


def add_card(bot, query):
    try:
        global _flash_cards
        _flash_cards.add_card()
    except Exception as e:
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text="Something went wrong when adding card: " + str(e)
        )
    reply_keyboard = [
        [InlineKeyboardButton('Search new word', callback_data=_DICT)],
        [InlineKeyboardButton('Go to falsh cards', callback_data=_GET_CARD)],
        [InlineKeyboardButton('Exit', callback_data=ConversationHandler.END)]
    ]
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text='Added to flash cards',
        reply_markup=InlineKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return _ENTRY_POINTS


def get_card(bot, query):
    try:
        global _flash_cards
        _flash_cards.next_card()
        word = _flash_cards.get_cur_word()
        reply_keyboard = [
            [InlineKeyboardButton('Show definition', callback_data=_SHOW_DEF)],
            [InlineKeyboardButton('Exit', callback_data=ConversationHandler.END)]
        ]
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=word,
            reply_markup=InlineKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
    except Exception as e:
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text="Something went wrong when getting card: " + str(e)
        )
    return _ENTRY_POINTS


def show_def(bot, query, conf):
    try:
        global _flash_cards
        word = _flash_cards.get_cur_word()
        definition = merriam_webster(word, conf['merriam_webster'])
        reply_keyboard = [
            [InlineKeyboardButton('See full definition', url='https://www.merriam-webster.com/dictionary/' + word)],
            [
                InlineKeyboardButton(emoji.emojize(':heavy_check_mark:'), callback_data=_ADD_CORRECT),
                InlineKeyboardButton('Next', callback_data=_GET_CARD),
            ],
            [InlineKeyboardButton('Exit', callback_data=ConversationHandler.END)]
        ]
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=definition,
            reply_markup=InlineKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
    except Exception as e:
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text="Something went wrong when getting definition: " + str(e)
        )
    return _ENTRY_POINTS


@has_access
def exit(update, context, conf):
    global _flash_cards
    _flash_cards.destory()
    update.message.reply_text('Exit Vocab Mode...')
    return ConversationHandler.END


def vocab_handler(conf):
    handler = ConversationHandler(
            entry_points=[CommandHandler('vocab', partial(vocab, conf=conf))],
            states={
                _DICT: [MessageHandler(Filters.text, partial(dictionary, conf=conf))],
                _ENTRY_POINTS: [CallbackQueryHandler(partial(entry_points, conf=conf))]
            },
            fallbacks=[CommandHandler('exit', partial(exit, conf=conf))]
    )
    return handler
