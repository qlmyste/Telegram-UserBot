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

    response = client.long_running_recognize(config=config, audio=audio)
    #print(response)
    op_result = response.result()
    result = op_result.results[0].alternatives[0]
    
    output = f"**Transcript:** {result.transcript}\n\n**Confidence:** __{round(result.confidence, 5)}__"
    await e.edit(output)
