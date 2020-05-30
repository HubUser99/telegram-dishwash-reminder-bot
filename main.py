import os
import json
import datetime

import constants

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import urllib3
http = urllib3.PoolManager()

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def help(update, context):
    """Send a message when the command /help is issued."""
    helpText = "/who - shows communist for today\n"
    helpText += "/who day/month/year - shows communist for the given day\n"
    helpText += "/who yesterday - shows communist for the yesterday"
    update.message.reply_text(helpText)

def who(update, context):
    people = ["Roma", "Nina", "Egor"]

    text = update.message.text.replace(" ", "")
    arg = getArgument(text)

    initDate = datetime.date(2020, 3, 31)
    dateNow = ''

    print(arg)

    if (len(arg) != 0):
        if (arg == "yesterday"):
           dateNow = datetime.date.today() - datetime.timedelta(days=1)
        else:
            argArray = arg.split('/')

            if (len(argArray) != 3):
                update.message.reply_text("Incorrect date format")
                return

            year = int(argArray[2])
            month = int(argArray[1])
            date = int(argArray[0])

            try:
                dateNow = datetime.date(year, month, date)
            except ValueError as error:
                update.message.reply_text(str(error))
                return
    else:
        dateNow = datetime.date.today() 
    
    delta = dateNow - initDate
    deltaDays = delta.days
    personIndex = deltaDays % 3
    update.message.reply_text(people[personIndex])

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def getArgument(text):
    # trim command itself
    arg = text[4:len(text)].strip()

    # trim name of the bot in the end, if called with it
    if (len(arg) >= 15):
        arg = arg[0:len(arg) - 15]
    
    return arg

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary

    token = os.getenv("BOT_TOKEN")

    print(token)

    updater = Updater(token=token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("who", who))
    
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
