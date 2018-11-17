"""
    Who's a good bot?
"""
import sys
import argparse
from functools import partial

from telegram.ext import Updater, CommandHandler, ConversationHandler, Filters, MessageHandler
import simplejson as json
import logging

from skills.term import term_handler
from skills.conversation import conversation_handler
from skills.spell import spell_handler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def help(bot, update):
    update.message.reply_text("Nice try...")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


class Bot:
    def __init__(self, conf):
        self.conf = conf
        self.updater = Updater(conf['telegram'])
        # Get the dispatcher to register handlers
        self.dp = self.updater.dispatcher
        self.set_skills()

    def set_skills(self):

        #self.dp.add_handler(ConversationHandler(entry_points=[CommandHandler("start", self.check_access)], states={}, fallbacks=[]))

        # on different commands - answer in Telegram
        #self.dp.add_handler(CommandHandler("help", partial(self.check_access, func=help)))
        #self.dp.add_handler(CommandHandler("term", partial(self.check_access, func=term)))
        self.dp.add_handler(term_handler(self.conf))
        self.dp.add_handler(spell_handler(self.conf))

        # on noncommand
        self.dp.add_handler(conversation_handler(self.conf))

        # log all errors
        self.dp.add_error_handler(error)

    def run(self):
        """
            Run bot.
        """
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
        print >> sys.stderr, '\nExiting by user request.\n'
        sys.exit(0)
