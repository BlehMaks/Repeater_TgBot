#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  7 17:20:19 2022

@author: Maksim Blekhshtein
"""
from time import sleep
from flask import Flask, request 
import telegram
from bot.config import bot_token, heroku_url

global bot, TOKEN #setting global vars
TOKEN = bot_token #using bot token from config
bot = telegram.Bot(token=TOKEN) #launching a bot object

bot_app = Flask(__name__) # start flask application

@bot_app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    #get the received message
    new_msg = telegram.Update.de_json(request.get_json(force=True), bot)

    #ids of who wrote message and of message itself
    chat_id = new_msg.message.chat_id
    msg_id = new_msg.message.message_id
    
    #what is in the message
    try:
        text = new_msg.message.text.encode('UTF-8').decode()
    except Exception:
        text = "Ha-ha, that's not a text or emoji"
    
    # print('received message: ', text) # debug
    
    # check if /start command was sent and generate response
    if text == '/start':
        welcome_msg = 'I am funny repeater bot, I will reply to your message \
            with your own text. I hope you will not get mad at me :)'
        bot.sendMessage(chat_id=chat_id, text=welcome_msg,\
                        reply_to_message_id=msg_id)
    else:
        try:
            bot.sendChatAction(chat_id=chat_id, action='typing')
            sleep(2)
            # reply to the msg with the same text
            bot.sendMessage(chat_id=chat_id, text=text, \
                            reply_to_message_id=msg_id)
        except Exception:
            # if something goes wrong
            error_msg = 'Something went wrong, sorry, I will not reply \
                to this properly'
            bot.sendMessage(chat_id=chat_id, text=error_msg, \
                            reply_to_message_id=msg_id)
    return 'ok'

@bot_app.route('/setwebhook', methods=['GET','POST'])
def setwebhook():
    # link the bot object to the app
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=heroku_url, HOOK=TOKEN))
    # check if this went ok
    if s:
        return('Webhook was set up properly')
    else:
        return('I broke webhook setting up')

@bot_app.route('/')
def index():
    return '.'

if __name__=='__main__':
    bot_app.run(threaded=True)