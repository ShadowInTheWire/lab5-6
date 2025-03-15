import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
#import configparser
import logging
import redis
from ChatGPT_HKBU import HKBU_ChatGPT

global redis1
global chatgpt

def main():
    # Load your token and create an Updater for your Bot
    # config = configparser.ConfigParser()
    # config.read('config.ini')
    
    #updater = Updater(token=config['TELEGRAM']['ACCESS_TOKEN'], use_context=True)
    updater = Updater(token=(os.environ['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher

   
    

    # Set up logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    # Initialize ChatGPT
    global chatgpt
    #chatgpt = HKBU_ChatGPT(config)
    chatgpt = HKBU_ChatGPT()
    # Register handlers
    # Commented out the echo handler as per your request
    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    # dispatcher.add_handler(echo_handler)

    # Dispatcher for ChatGPT
    chatgpt_handler = MessageHandler(Filters.text & (~Filters.command), equiped_chatgpt)
    dispatcher.add_handler(chatgpt_handler)

    # On different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help_command))
    
    # New command handler for /hello
    dispatcher.add_handler(CommandHandler("hello", hello))

    # Start the bot
    updater.start_polling()
    updater.idle()

def equiped_chatgpt(update: Update, context: CallbackContext) -> None:
    global chatgpt
    
    chatgpt = HKBU_ChatGPT()
    reply_message = chatgpt.submit(update.message.text)
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Helping you helping you.')

def add(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try:
        global redis1
        logging.info(context.args[0])
        msg = context.args[0]  # /add keyword <-- this should store the keyword
        redis1.incr(msg)
        update.message.reply_text(
            'You have said ' + msg + ' for ' + redis1.get(msg) + ' times.'
        )
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')

# New hello function
def hello(update: Update, context: CallbackContext) -> None:
    """Send a greeting message when the command /hello is issued."""
    if context.args:
        name = ' '.join(context.args)  # Join all arguments to handle multi-word names
        update.message.reply_text(f'Good day, {name}!')
    else:
        update.message.reply_text('Usage: /hello <name>')

if __name__ == '__main__':
    main()
