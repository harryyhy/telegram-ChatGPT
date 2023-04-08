from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import configparser
import logging
import redis
import os

import sys
sys.path.append('/')

import openai
import json

global redis1
openai.api_key = "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"

def main():
# Load your token and create an Updater for your Bot
    # config = configparser.ConfigParser()
    # config.read('config.ini')
    # updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    # dispatcher = updater.dispatcher

    updater = Updater(token=(os.environ['ACCESS_TOKEN']), use_context=True)
    # updater = Updater(token="6272770771:AAErGQoJw6Yuw2HVGMH6Tp_KsTZiLHE8BzY", use_context=True)
    dispatcher = updater.dispatcher

    global redis1
    # redis1 = redis.Redis(host=(config['REDIS']['HOST']), 
    #                     password=(config['REDIS']['PASSWORD']), 
    #                     port=(config['REDIS']['REDISPORT']))

    redis1 = redis.Redis(host=(os.environ['HOST']), password=
                            (os.environ['PASSWORD']), port=(os.environ['REDISPORT']), ssl=True)
    # redis1 = redis.Redis(host="chatbot-chatgpt.redis.cache.windows.net", 
    #                     password="VniyXvnT2pUiqKKA15tObD7Pij8oo1kqOAzCaOFMloU=", 
    #                     port=6380, ssl=True)
                        
    # You can set this logging module, so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

    # register dispatchers to handle message
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), chat))     # normal chat
    dispatcher.add_handler(CommandHandler("newchat", newchat))    # to create a new chat
    dispatcher.add_handler(CommandHandler("history", history))    # show all the chats before
    dispatcher.add_handler(CommandHandler("help", help))        # show helps

    # To start the bot:
    updater.start_polling()
    updater.idle()

# error handler
def error(update, context):
    logging.warning('Update "%s" caused error "%s"', update, context.error)
    reply = "Error: " + str(context.error) + "\nTry again now!"
    update.message.reply_text(reply)

# normal chat
def chat(update, context):
    # log
    logging.info("Update: " + str(str(update['message'])))

    content = update['message']['text'] # user input
    ms = [] # all the message, may includes chats before

    key = "user:" + str(update['message']['chat']['id'])    # redis key, in this format 'user:${telegram_id}'

    # if user is exist, get history, else initialize a new chat
    if redis1.exists(key):
        ms.extend(json.loads(redis1.get(key)))  # extend is for merge 2 lists, append is unavaiable for merge
    ms.append({"role": "user", "content": content})

    # invoke ChatGPT
    rsp = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = ms
    )

    # include the latest response and set it into redis
    ms.append({"role": "assistant", "content": rsp["choices"][0]["message"]["content"]})
    redis1.set(key, json.dumps(ms))

    # reply to user
    reply_message = rsp["choices"][0]["message"]["content"] 

    # add help info
    reply_message += "\n\n/help to show tips"

    context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)

def help(update: Update, context: CallbackContext) -> None:
    reply = """
/help : get help from bot\n
/newchat : begin a new bot\n
/history : get history of this chat
    """
    update.message.reply_text(reply)

# begin a new chat
def newchat(update: Update, context: CallbackContext) -> None:
    key = "user:" + str(update['message']['chat']['id'])
    redis1.delete(key)
    update.message.reply_text("Begin your new chat right now!")

# get history from redis and combine them in readable way
def history(update: Update, context: CallbackContext) -> None:
    key = "user:" + str(update['message']['chat']['id'])
    if not redis1.exists(key):
        update.message.reply_text("No history, begin your chat right now!")
        return
    ms = json.loads(redis1.get(key))
    reply = ""
    for m in ms:
        if m['role'] == 'user':
            reply += "You:\n" + m['content'] + '\n\n'
        else:
            reply += "Bot:\n" + m['content'] + '\n\n\n'

    update.message.reply_text(reply)


if __name__ == '__main__':
    main()