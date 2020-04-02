import os, json, requests, time
from userbot import BOTLOG, bot, BOTLOG_CHATID, CMD_HELP
from userbot.events import register
from userbot import AUDIOTAG_API as API_CODE

api_url = 'https://audiotag.info/api'

@register(outgoing=True, pattern=r"^\.audio$")
async def audiotag(at):
  if API_CODE is None:
    await at.edit("We don't support magic! No API Code! Take it from audiotag.info")
    return
  message = await at.get_reply_message()
  if message.audio or message.voice:
    file = message.audio or message.voice
    at.edit("Getted audio file")
    file = await bot.download_file(file, "audio.mp3")
    at.edit("Downloaded")
    os.system("ffmpeg -i audio.mp3 -ar 8000 -ac 1 -vn converted.wav")
    at.edit("Converted")
    payload = {'action': 'identify', 'apikey': API_CODE}
    at.edit("Payload complete")
    result = requests.post(api_url,data=payload,files={'file': open(filename, 'rb')})
    at.edit("Result getted")
    at.edit(result.text)
