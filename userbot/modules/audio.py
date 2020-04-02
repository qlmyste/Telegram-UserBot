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
    await at.edit("Getted audio file")
    file = await bot.download_file(file, "audio.mp3")
    await at.edit("Downloaded")
    await os.system("ffmpeg -i audio.mp3 -ar 8000 -ac 1 -vn converted.wav")
    await at.edit("Converted")
    payload = {'action': 'identify', 'apikey': API_CODE}
    await at.edit("Payload complete")
    result = requests.post(api_url,data=payload,files={'file': open(filename, 'rb')})
    await at.edit("Result getted")
    await at.edit(result.text)
