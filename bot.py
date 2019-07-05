"""
    Who's a good bot?
"""
import sys
import argparse
from functools import partial

import logging
import simplejson as json
from telegram.ext import Updater, CommandHandler, ConversationHandler, Filters, MessageHandler

from skills.term import term_handler
from skills.conversation import conversation_handler
from skills.spell import spell_handler
from skills.lyrics import lyrics_handler
from skills.tele import tele_handler
from skills.utils import has_access

from database.utils import setup_db
from service.utils import start_service

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

@has_access
def help(bot, update, conf):
    """Send a message when the command /help is issued."""
    update.message.reply_text((
        "/term   Enter terminal mode connected to server.\n"
        "/tele [--clean] [--kill PID]   Check scripts status run with tele.\n"
        "/lyrics [KEYWORDS]   Search lyrics based on keywords.\n"
        "/spell [KEYWORD]   Spell check and return possible corrections."
    ))

def help_handler(conf):
    handler = CommandHandler("help", partial(help, conf=conf))
    return handler

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


class Bot:
    def __init__(self, conf):
        self.conf = conf
        self.updater = Updater(conf['telegram'])
        # Get the dispatcher to register handlers
        self.dp = self.updater.dispatcher

        # Set up databases
        setup_db(conf['databases'])

        # Set up skills
        self.set_skills()

    def set_skills(self):
        # on different commands - answer in Telegram
        self.dp.add_handler(help_handler(self.conf))
        self.dp.add_handler(term_handler(self.conf))
        self.dp.add_handler(spell_handler(self.conf))
        self.dp.add_handler(lyrics_handler(self.conf))
        self.dp.add_handler(tele_handler(self.conf))

        # on noncommand
        self.dp.add_handler(conversation_handler(self.conf))

        # log all errors
        self.dp.add_error_handler(error)

    def run(self):
        """
            Run bot.
        """
        # Start BionicPhoenixService
        start_service(self.conf['telegram'], self.conf['white_list'][0])

        # Start the Bot
        self.updater.start_polling()

        # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
        # SIGABRT. This should be used most of the time, since start_polling() is
        # non-blocking and will stop the bot gracefully.
        self.updater.idle()

def main():
    arg_parser = argparse.ArgumentParser('Bionic Phoenix is the best Phoenix')
    arg_parser.add_argument('-c', '--config', help = 'Config file')
    args = arg_parser.parse_args()

    if args.config == None:
        print("Config file required as argument")
        sys.exit(0)

    config = None
    try:
        with open(args.config, 'r') as f:
            config = json.load(f)
    except Exception as e:
        print("Error occur when reading config: " + str(e))
        sys.exit(1)

    bot = Bot(config)
    bot.run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nExiting by user request.\n', file=sys.stderr)
        sys.exit(0)
