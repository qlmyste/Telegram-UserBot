# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing various scrapers. """

import os
from html import unescape
from re import findall
from shutil import rmtree
from urllib.error import HTTPError
#from subprocess import call
from emoji import get_emoji_regexp
from google_images_download import google_images_download
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googletrans import LANGUAGES, Translator
from gtts import gTTS
from pytube import YouTube
from pytube.helpers import safe_filename
from requests import get
from search_engine_parser import GoogleSearch
from urbandict import define
from wikipedia import summary
from wikipedia.exceptions import DisambiguationError, PageError
from random_words import RandomWords

from userbot import (BOTLOG, BOTLOG_CHATID, CMD_HELP, CURRENCY_API,
                     YOUTUBE_API_KEY, bot)
from userbot.events import register

LANG = "en"


@register(outgoing=True, pattern="^.img (.*)")
async def img_sampler(event):
    """ For .img command, search and return images matching the query. """
    await event.edit("Processing...")
    query = event.pattern_match.group(1)
    lim = findall(r"lim=\d+", query)
    try:
        lim = lim[0]
        lim = lim.replace("lim=", "")
        query = query.replace("lim=" + lim[0], "")
    except IndexError:
        lim = str(2)
    if os.path.isdir("downloads") is False:
      os.mkdir("downloads")
    os.system("./bing.py -nn -l " + lim + " -u https://www.bing.com/images/search?q=" + query)
    #TODO: make a sending as album
    for filename in os.listdir("downloads"):
      #paths = 'downloads/' + filename + ', '
      await event.client.send_file(event.chat.id, file='downloads/' + filename)
    rmtree("downloads")
    await event.delete()

@register(outgoing=True, pattern="^.ranimg")
async def img_sam(event):
    """ For .img command, search and return images matching the query. """
    await event.edit("Processing...")
    query = RandomWords().random_word()
    await event.edit("**Random word is: **" + query)
    if os.path.isdir("downloads") is False:
      os.mkdir("downloads")
    os.system("./bing.py -nn -l " + "2" + " -u https://www.bing.com/images/search?q=" + query)
    #TODO: make a sending as album
    for filename in os.listdir("downloads"):
      #paths = 'downloads/' + filename + ', '
      await event.client.send_file(event.chat.id, file='downloads/' + filename)
    rmtree("downloads")
    
@register(outgoing=True, pattern=r"^.wiki (.*)")
async def wiki(wiki_q):
    """ For .google command, fetch content from Wikipedia. """
    match = wiki_q.pattern_match.group(1)
    try:
        summary(match)
    except DisambiguationError as error:
        await wiki_q.edit(f"Disambiguated page found.\n\n{error}")
        return
    except PageError as pageerror:
        await wiki_q.edit(f"Page not found.\n\n{pageerror}")
        return
    result = summary(match)
    if len(result) >= 4096:
        file = open("output.txt", "w+")
        file.write(result)
        file.close()
        await wiki_q.client.send_file(
            wiki_q.chat_id,
            "output.txt",
            reply_to=wiki_q.id,
            caption="`Output too large, sending as file`",
        )
        if os.path.exists("output.txt"):
            os.remove("output.txt")
        return
    await wiki_q.edit("**Search:**\n`" + match + "`\n\n**Result:**\n" + result)
    if BOTLOG:
        await wiki_q.client.send_message(
            BOTLOG_CHATID, f"Wiki query {match} was executed successfully")


@register(outgoing=True, pattern="^.ud (.*)")
async def urban_dict(ud_e):
    """ For .ud command, fetch content from Urban Dictionary. """
    await ud_e.edit("Processing...")
    query = ud_e.pattern_match.group(1)
    try:
        define(query)
    except HTTPError:
        await ud_e.edit(f"Sorry, couldn't find any results for: {query}")
        return
    mean = define(query)
    deflen = sum(len(i) for i in mean[0]["def"])
    exalen = sum(len(i) for i in mean[0]["example"])
    meanlen = deflen + exalen
    if int(meanlen) >= 0:
        if int(meanlen) >= 4096:
            await ud_e.edit("`Output too large, sending as file.`")
            file = open("output.txt", "w+")
            file.write("Text: " + query + "\n\nMeaning: " + mean[0]["def"] +
                       "\n\n" + "Example: \n" + mean[0]["example"])
            file.close()
            await ud_e.client.send_file(
                ud_e.chat_id,
                "output.txt",
                caption="`Output was too large, sent it as a file.`")
            if os.path.exists("output.txt"):
                os.remove("output.txt")
            await ud_e.delete()
            return
        await ud_e.edit("Text: **" + query + "**\n\nMeaning: **" +
                        mean[0]["def"] + "**\n\n" + "Example: \n__" +
                        mean[0]["example"] + "__")
        if BOTLOG:
            await ud_e.client.send_message(
                BOTLOG_CHATID, "ud query " + query + " executed successfully.")
    else:
        await ud_e.edit("No result found for **" + query + "**")


@register(outgoing=True, pattern=r"^.tts(?: |$)([\s\S]*)")
async def text_to_speech(query):
    """ For .tts command, a wrapper for Google Text-to-Speech. """
    textx = await query.get_reply_message()
    message = query.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await query.edit("`Give a text or reply to a "
                         "message for Text-to-Speech!`")
        return

    try:
        gTTS(message, LANG)
    except AssertionError:
        await query.edit('The text is empty.\n'
                         'Nothing left to speak after pre-precessing, '
                         'tokenizing and cleaning.')
        return
    except ValueError:
        await query.edit('Language is not supported.')
        return
    except RuntimeError:
        await query.edit('Error loading the languages dictionary.')
        return
    tts = gTTS(message, LANG)
    tts.save("k.mp3")
    with open("k.mp3", "rb") as audio:
        linelist = list(audio)
        linecount = len(linelist)
    if linecount == 1:
        tts = gTTS(message, LANG)
        tts.save("k.mp3")
    with open("k.mp3", "r"):
        await query.client.send_file(query.chat_id, "k.mp3", voice_note=True)
        os.remove("k.mp3")
        if BOTLOG:
            await query.client.send_message(
                BOTLOG_CHATID, "tts of " + message + " executed successfully!")
        await query.delete()


@register(outgoing=True, pattern=r"^.trt(?: |$)([\s\S]*)")
async def translateme(trans):
    """ For .trt command, translate the given text using Google Translate. """
    translator = Translator()
    textx = await trans.get_reply_message()
    message = trans.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await trans.edit("`Give a text or reply "
                         "to a message to translate!`")
        return

    try:
        reply_text = translator.translate(deEmojify(message), dest=LANG)
    except ValueError:
        await trans.edit("Invalid destination language.")
        return

    source_lan = LANGUAGES[f'{reply_text.src.lower()}']
    transl_lan = LANGUAGES[f'{reply_text.dest.lower()}']
    reply_text = f"**Source ({source_lan.title()}):**`\n{message}`**\n\
\nTranslation ({transl_lan.title()}):**`\n{reply_text.text}`"

    await trans.client.send_message(trans.chat_id, reply_text)
    await trans.delete()
    if BOTLOG:
        await trans.client.send_message(
            BOTLOG_CHATID,
            f"Translate query {message} was executed successfully",
        )


@register(pattern="^.lang (.*)", outgoing=True)
async def lang(value):
    """ For .lang command, change the default langauge of userbot scrapers. """
    global LANG
    LANG = value.pattern_match.group(1)
    await value.edit("Default language changed to **" + LANG + "**")
    if BOTLOG:
        await value.client.send_message(
            BOTLOG_CHATID, "Default language changed to **" + LANG + "**")

@register(outgoing=True, pattern=r"^.cr (\S*) ?(\S*) ?(\S*)")
async def currency(cconvert):
    """ For .cr command, convert amount, from, to. """
    amount = cconvert.pattern_match.group(1)
    currency_from = cconvert.pattern_match.group(3).upper()
    currency_to = cconvert.pattern_match.group(2).upper()
    data = get(
        f"https://free.currconv.com/api/v7/convert?apiKey={CURRENCY_API}&q={currency_from}_{currency_to}&compact=ultra"
    ).json()
    result = data[f'{currency_from}_{currency_to}']
    result = float(amount) / float(result)
    result = round(result, 5)
    await cconvert.edit(
        f"{amount} {currency_to} is:\n`{result} {currency_from}`")


def deEmojify(inputString):
    """ Remove emojis and other non-safe characters from string """
    return get_emoji_regexp().sub(u'', inputString)


CMD_HELP.update({"scrapers": ['Scrapers',
    " - `.img <query> lim=<n>`: Do an Image Search on Bing and send n results. Default is 2.\n"
    " - `.ranimg`: Do an Random Image Search on Bing and send 2 results
    " - `.google <query>`: Search Google for query (argument or reply).\n"
    " - `.wiki <query>`: Search Wikipedia for query.\n"
    " - `.ud <query>`: Search on Urban Dictionary for query.\n"
    " - `.tts <query>`: Text-to-Speech the query (argument or reply) to the saved language.\n"
    " - `.trt <query>`: Translate the query (argument or reply) to the saved language.\n"
    " - `.lang <lang>`: Changes the default language of trt and TTS modules.\n"
    " - `.wolfram <query>: Get answers to questions using WolframAlpha Spoken Results API."]
})
