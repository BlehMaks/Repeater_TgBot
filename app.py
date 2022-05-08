#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  7 17:20:19 2022

@author: Maksim Blekhshtein
"""
from flask import Flask, request 
import telegram
from bot.config import bot_token, bot_name, heroku_url

global bot, TOKEN #setting global vars
TOKEN = bot_token #using bot token from config
bot = telegram.Bot(token=TOKEN) #launching a bot object

app = Flask(__name__) # start flask application

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    #get the received message
    new_msg = telegram.Update.de_json(request.get_json(force=True), bot)
    
    #ids of who wrote message and of message itself
    chat_id = new_msg.message.chat_id
    msg_id = new_msg.message.message_id
    
    #what is in the message
    text = new_msg.message.text.encode('UTF-8').decode()
    
    # print('received message: ', text) # debug
    
    # check if /start command was sent
    if text == '/start':
        welcome_msg = 'I am funny repeater bot, I will reply to your message \
            with your own text. I hope you will not get mad at me :) '
        bot.sendMessage(chat_id=chat_id, text=welcome_msg,\
                        reply_to_message_id=msg_id)
        
    else:
        try:
            # reply to the msg with the same text
            bot.sendMessage(chat_id=chat_id, text=text, \
                            reply_to_message_id=msg_id)
            
        except Exception:
            # if something goes wrong
            error_msg = 'Fuck, something went wrong, sorry, I will not reply \
                to this properly'
            bot.sendMessage(chat_id=chat_id, text=error_msg, \
                            reply_to_message_id=msg_id)
    return

@app.route('/setwebhook', methods=['GET','POST'])
def setwebhook():
    # link the bot object to the app
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=heroku_url, HOOK=TOKEN))
    # check if this went ok
    if s:
        print('webhook was set up properly')
    else:
        print('I fucked up webhook')
    
    return

@app.route('/')
def index():
    return '.'

if __name__=='__main__':
    app.run(threaded=True)