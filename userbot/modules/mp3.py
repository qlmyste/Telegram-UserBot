from userbot import BOTLOG, bot, BOTLOG_CHATID, CMD_HELP
from userbot.events import register
from userbot.utils import parse_arguments
from moviepy import editor as mp
import os

@register(outgoing=True, pattern=r"^\.mp3$")
async def mp3(e):
  message = await e.get_reply_message()
  if message.audio or message.voice:
    file = message.audio or message.voice
    file = await bot.download_file(file, "voice.mp3")
    await e.edit("**Sending...**")
    await e.client.send_file(e.chat_id,
                            f'voice.mp3',
                            reply_to=message)
    os.remove(f'voice.mp3')
  if message.video:
    video = message.video
    await e.edit("**Downloading...**")
    video = await bot.download_file(video, "video.mp4")
    await e.edit("**Converting video...**")
    clip = mp.VideoFileClip('video.mp4')
    clip.audio.write_audiofile(f'video.mp3')
    await e.edit("**Sending mp3...**")
    await e.client.send_file(e.chat.id,
                             f'video.mp3',
                             reply_to=message)
  else:
         await e.edit("**Bot doesn't support magic! Use video or voice message.**")
         return
      
@register(outgoing=True, pattern=r"^\.voice$")
async def vc(v):
    if message.audio or message.voice:
      file = message.audio or message.voice
      file = await bot.download_file(file, "voice.mp3")
      await v.edit("**Sending...**")
      await v.client.send_file(v.chat_id,
                             f'voice.mp3',
                             reply_to=message, voice_note=True)
      os.remove(f'voice.mp3')
  
  CMD_HELP.update({
    ".mp3":
    "Convert a voice message to a mp3 and send it."
})
  CMD_HELP.update({
    ".voice":
    "Convert music message to voice message."
})
