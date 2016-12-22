# -*- coding: utf-8 -*-

import configparser
from urllib.parse import quote_plus
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, CallbackQueryHandler
from telegram import InlineQueryResultArticle, ChatAction, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
from uuid import uuid4
import subprocess
import time
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


config = configparser.ConfigParser()
config.read('bot.ini')

updater = Updater(token=config['KEYS']['bot_api'])
dispatcher = updater.dispatcher


def start(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    bot.sendMessage(chat_id=update.message.chat_id, 
                    text="Hi. I'm Hunter's Jenkins Bot! You can use me to start builds, assuming your name is @hunter_bruhh! If not, then I'm not much use to you right now! Maybe he'll implement some cool stuff later!")
    if update.message.from_user.id != int(config['ADMIN']['id']):
        bot.sendChatAction(chat_id=update.message.chat_id,
                           action=ChatAction.TYPING)
        time.sleep(1)
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="It seems like you aren't allowed to use me. :(")
        bot.sendChatAction(chat_id=update.message.chat_id,
                           action=ChatAction.TYPING)
    else:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Sup @hunter_bruhh ! \nHere's a list of commands for you to use\n/build to start the build process\n/changelog 'text' to set the changelog\n/sync to set sync to on/off\n/clean to set clean to on/off\n/start to see this message :)")
        bot.sendChatAction(chat_id=update.message.chat_id,
                           action=ChatAction.TYPING)
                           
def choosebuild(bot, update):
    if update.message.from_user.id == int(config['ADMIN']['id']):
        keyboard = [[InlineKeyboardButton("Without Paramaters", callback_data='build')],

                    [InlineKeyboardButton("With Parameters", callback_data='buildWithParameters')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Please choose a build style:', reply_markup=reply_markup)

def sync(bot, update):
    if update.message.from_user.id == int(config['ADMIN']['id']):
        keyboard = [[InlineKeyboardButton("YES", callback_data='syncon')],

                    [InlineKeyboardButton("NO", callback_data='syncoff')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Would you like to sync on a new build?:', reply_markup=reply_markup)
        
def clean(bot, update):
    if update.message.from_user.id == int(config['ADMIN']['id']):
        keyboard = [[InlineKeyboardButton("YES", callback_data='cleanon')],

                    [InlineKeyboardButton("NO", callback_data='cleanoff')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Would you like to clean on a new build?:', reply_markup=reply_markup)

def buildwithparams(bot, update, query):
    query = update.callback_query
    bot.sendMessage(chat_id=query.message.chat_id,
                    text="You have selected the 'buildWithParameters option, this will include a custom changelog with your build, and will specify whether to sync & clean or not", 
                    parse_mode="Markdown")
    user_id = update.callback_query.from_user.id
    try:
        cg
    except NameError:
        bot.sendMessage(chat_id=query.message.chat_id,
                        text="You have selected the 'buildWithParameters option, but the changelog is empty. Please use /changelog + 'text' to provide a changlog for your users.", 
                        parse_mode="Markdown")
        return 1
    try:
        syncparam
    except NameError:
        bot.sendMessage(chat_id=query.message.chat_id,
                text="You have selected the 'buildWithParameters option, but have not specified whether you would like to sync before building. Please use /sync to do so.", 
                parse_mode="Markdown")
        return 1
    try:
        cleanparam
    except NameError:
        bot.sendMessage(chat_id=query.message.chat_id,
                text="You have selected the 'buildWithParameters option, but have not specified whether you would like to clean before building. Please use /clean to do so.", 
                parse_mode="Markdown")
        return 1
    if cg:
        if syncparam:
            if cleanparam:
                global changelog
                changelog = quote_plus('cg')
                command_string = "https://jenkins.hunterbruhh.me/job/halogenOS/buildWithParameters?token=bruhhrockztheop2buildsbro&changelog=" + cg + "&SYNC=" + syncparam + "&CLEAN=" + cleanparam
                command = "curl --user hunterbruhh:09131999 " + "'" + command_string + "'"
                print (command)
                if user_id == int(config['ADMIN']['id']):
                    bot.sendChatAction(chat_id=query.message.chat_id,
                                       action=ChatAction.TYPING)
                    output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    output = output.stdout.read().decode('utf-8')
                    output = '`{0}`'.format(output)
                
                    bot.sendMessage(chat_id=query.message.chat_id,
                                    text=output, 
                                    parse_mode="Markdown")
            else:
                bot.sendMessage(chat_id=query.message.chat_id,
                                text="You have selected the 'buildWithParameters option, but have not specified whether you would like to clean before building. Please use /clean to do so.", 
                                parse_mode="Markdown")
        else:
            bot.sendMessage(chat_id=query.message.chat_id,
                            text="You have selected the 'buildWithParameters option, but have not specified whether you would like to sync before building. Please use /sync to do so.", 
                            parse_mode="Markdown")
    else:
        bot.sendMessage(chat_id=query.message.chat_id,
                            text="You have selected the 'buildWithParameters option, but the changelog is empty. Please use /changelog + 'text' to provide a changlog for your users.", 
                            parse_mode="Markdown")
                            
                        
def buildwithoutparams(bot, update, query):
    user_id = update.callback_query.from_user.id
    command_string = "https://jenkins.hunterbruhh.me/job/halogenOS/buildWithParameters?token=bruhhrockztheop2buildsbro"
    command = "curl --user hunterbruhh:09131999 " + "'" + command_string + "'"
    print (command)
    if user_id == int(config['ADMIN']['id']):
        bot.sendChatAction(chat_id=query.message.chat_id,
                           action=ChatAction.TYPING)
        output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = output.stdout.read().decode('utf-8')
        output = '`{0}`'.format(output)

        bot.sendMessage(chat_id=query.message.chat_id,
                        text=output, parse_mode="Markdown")
                            
def changelog(bot, update, args):
        if update.message.from_user.id == int(config['ADMIN']['id']):
            global cg
            user = update.message.from_user
            
            str_args = ' '.join(args)
            if str_args != "":
                update.message.reply_text('Changelog updated: ' + "'" + str_args + "'")
                cgs = '%20'.join(args)
                cg = cgs
                print ("Changelog set to " + "'" + cg + "'")
            else:
                bot.sendMessage(chat_id=update.message.chat_id,
                                text="You cannot provide an empty changelog.", 
                                parse_mode="Markdown")

def button(bot, update, direct=True):
        user_id = update.callback_query.from_user.id
        if user_id == int(config['ADMIN']['id']):
            query = update.callback_query

            selected_button = query.data
            global cleanparam
            global syncparam
            if selected_button == 'buildWithParameters':
                bot.editMessageText(text="Selected option: With Paramaters",
                                    chat_id=query.message.chat_id,
                                    message_id=query.message.message_id)
                buildwithparams(bot, update, query)
            if selected_button == 'build':
                bot.editMessageText(text="Selected option: Without Paramaters",
                                    chat_id=query.message.chat_id,
                                    message_id=query.message.message_id)
                buildwithoutparams(bot, update, query)
            if selected_button == 'syncon':
                bot.editMessageText(text="Selected option: YES",
                                    chat_id=query.message.chat_id,
                                    message_id=query.message.message_id)
                syncparam = "true"
                bot.sendMessage(chat_id=query.message.chat_id,
                                text="Sync set to true", 
                                parse_mode="Markdown")
            if selected_button == 'syncoff':
                bot.editMessageText(text="Selected option: NO",
                                    chat_id=query.message.chat_id,
                                    message_id=query.message.message_id)
                syncparam = "false"
                bot.sendMessage(chat_id=query.message.chat_id,
                                text="Sync set to false", 
                                parse_mode="Markdown")
            if selected_button == 'cleanon':
                bot.editMessageText(text="Selected option: YES",
                                    chat_id=query.message.chat_id,
                                    message_id=query.message.message_id)
                cleanparam = "true"
                bot.sendMessage(chat_id=query.message.chat_id,
                                text="Clean set to true", 
                                parse_mode="Markdown")
            if selected_button == 'cleanoff':
                bot.editMessageText(text="Selected option: NO",
                                    chat_id=query.message.chat_id,
                                    message_id=query.message.message_id)
                cleanparam = "false"
                bot.sendMessage(chat_id=query.message.chat_id,
                                text="Clean set to false", 
                                parse_mode="Markdown")
        else:
                bot.sendMessage(chat_id=query.message.chat_id,
                                text="You trying to spam me bro?", 
                                parse_mode="Markdown")
        return False
            
def inlinequery(bot, update):
    query = update.inline_query.query
    o = execute(query, update, direct=False)
    results = list()

    results.append(InlineQueryResultArticle(id=uuid4(),
                                            title=query,
                                            description=o,
                                            input_message_content=InputTextMessageContent(
                                            '*{0}*\n\n{1}'.format(query, o),
                                            parse_mode="Markdown")))

    bot.answerInlineQuery(update.inline_query.id, results=results, cache_time=10)


start_handler = CommandHandler('start', start)
sync_handler = CommandHandler('sync', sync)
clean_handler = CommandHandler('clean', clean)
build_handler = CommandHandler('build', choosebuild)
changelog_handler = CommandHandler('changelog', changelog,  pass_args=True)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(sync_handler)
dispatcher.add_handler(clean_handler)
dispatcher.add_handler(build_handler)
dispatcher.add_handler(changelog_handler)
dispatcher.add_handler(CallbackQueryHandler(button))
dispatcher.add_handler(InlineQueryHandler(inlinequery))
dispatcher.add_error_handler(error)

updater.start_polling()
updater.idle()
