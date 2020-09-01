import io
import os

import speech_recognition as sr

from userbot import BOTLOG, BOTLOG_CHATID, bot, CMD_HELP
from userbot.events import register
from userbot.utils import parse_arguments


@register(outgoing=True, pattern=r"^\.stt(\s+[\s\S]+|$)")
async def speech_to_text(e):
    opts = e.pattern_match.group(1) or ""
    args, _ = parse_arguments(opts, ['lang'])

    await e.edit("**Transcribing...**")

    message = await e.get_reply_message()
    file = message.audio or message.voice

    if not file:
        await e.edit("**No audio file specified**", delete_in=3)
        return

    file = await bot.download_file(file)
    r = sr.Recognizer()
    with sr.AudioFile(file) as source:
        audio_text = r.listen(source)
    try:
        text = r.recognize_google(audio_text)
        print('Converting audio transcripts into text ...')
        await e.edit(text)
    except:
        await e.edit("Unknown error")
        return
