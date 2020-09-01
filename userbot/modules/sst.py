import io
import os

from google.cloud import speech_v1
from google.cloud.speech_v1 import enums

from userbot import BOTLOG, BOTLOG_CHATID, STTClient, stt, bot, CMD_HELP
from userbot.events import register
from userbot.utils import parse_arguments

DEFAULT_LANG = "en-US"


@register(outgoing=True, pattern=r"^\.stt(\s+[\s\S]+|$)")
async def speech_to_text(e):
    client = speech_v1.SpeechClient()
    opts = e.pattern_match.group(1) or ""
    args, _ = parse_arguments(opts, ['lang'])

    lang = args.get('lang', DEFAULT_LANG)
    await e.edit("**Transcribing...**")

    message = await e.get_reply_message()
    file = message.audio or message.voice

    if not file:
        await e.edit("**No audio file specified**", delete_in=3)
        return

    file = await bot.download_file(file)

    #content = io.BytesIO(file)
    audio = {'content': file}

    config = {
        'encoding':enums.RecognitionConfig.AudioEncoding.OGG_OPUS,
        'sample_rate_hertz':16000,
        'language_code':lang
    }
    res = ''
    conf = 0
    response = client.recognize(config, audio)
    for result in response.results:
       alternative = result.alternatives[0]
       res = alternative.transcript
       conf = alternative.confidence
    output = f"**Transcript:** {res}\n\n**Confidence:** __{round(conf, 5)}__"
    await e.edit(output)
