#!/usr/bin/python3
"""This implements a Telegram bot which can control a private home lamp."""

from typing import Set, Callable

import json
import logging

import telegram.ext as tgext
import telegram as tg
import requests

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def start(update: tg.Update, context: tgext.CallbackContext):
    """
    When we receice the command, /start, we will send a starting message and 
    mark up a keyboard.
    """
    custom_keyboard = [['Turn on the light'], ['Turn off the light']]
    reply_markup = tg.ReplyKeyboardMarkup(custom_keyboard)
    
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="I'm a bot, please talk to me!",
                             reply_markup=reply_markup)


def make_control_light(valid_user: Set[int], lamp_url: str, auth: str
                       ) -> Callable[[tg.Update, tgext.CallbackContext], None]:
    
    
    valid_message = {
        'Turn on': 'turn_on',
        'Turn on the light': 'turn_on',
        'Turn off': 'turn_off',
        'Turn off the light': 'turn_off'
    }
    
    def control_light(update: tg.Update, context: tgext.CallbackContext):
        """ 
        If our valid user send us message using keyboard, we will control the light 
        according to the message we receive.
        """
        
        if update.message.text in valid_message and update.effective_user.id in valid_user:

            response = requests.post(lamp_url,
                                     json={
                                         'what':
                                         valid_message[update.message.text],
                                         'auth': auth
                                     }).json()
            if response.get('status') == 'ok':
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text='Done!')
            elif response.get('status') is None:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text='LampGateWay is broken!!')
            else:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=response['status'])
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text='INVALID MESSAGE')

    return control_light


def main():
    with open('config.json') as json_file:
        config = json.load(json_file)
    updater = tgext.Updater(token=config['token'], use_context=True)
    valid_user: Set[int] = set(config['valid_user'])
    lamp_url = config['url']
    auth = config['auth']

    start_handler = tgext.CommandHandler('start', start)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(start_handler)

    control_light_handler = tgext.MessageHandler(
        tgext.Filters.text, make_control_light(valid_user, lamp_url, auth))
    dispatcher.add_handler(control_light_handler)

    updater.start_polling()


if __name__ == '__main__':
    main()