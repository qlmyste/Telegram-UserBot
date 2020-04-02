import os, json, requests, time
from userbot import CMD_HELP
from userbot.events import register
from userbot import AUDIOTAG_API as API_CODE

api_url = 'https://audiotag.info/api'

@register(outgoing=True, pattern=r"^\.audio (\S*)")
async def audiotag(at):
  if API_CODE is none:
    await at.edit("We don't support magic! No API Code! Take it from audiotag.info")
  message = await at.get_reply_message()
  if message.audio or message.voice:
    file = message.audio or message.voice
    file = await bot.download_file(file, "audio.mp3")
    os.system("ffmpeg -i audio.mp3 -ar 8000 -ac 1 -vn converted.wav")
    payload = {'action': 'identify', 'apikey': API_CODE}
    result = requests.post(api_url,data=payload,files={'file': open(filename, 'rb')})
    at.edit(result.text)
