import os

from pytube import YouTube
from pytube.helpers import safe_filename

from userbot import CMD_HELP
from userbot.events import register
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
from os import environ
from PIL import Image
global msg_for_percantage
@register(outgoing=True, pattern=r"^\.ytmp3 (\S*)")
async def youtube_mp3(ytmp3):
    if environ.get("isSuspended") == "True":
        return
    reply_message = await ytmp3.get_reply_message()
    url = ytmp3.pattern_match.group(1)

    await yt.edit("**Processing...**")

    video = YouTube(url)
    stream = video.streams.filter(only_audio=True, mime_type="audio/webm").last()
    os.system(f"wget -q -O 'picture.jpg' {video.thumbnail_url}")
    await ytmp3.edit("**Downloading audio...**")
    stream.download(filename=f'{safe_filename(video.title)}')
    await ytmp3.edit("**Converting to mp3...**")
    os.system(f"ffmpeg -loglevel panic -i '{safe_filename(video.title)}.webm' -vn -ab 128k -ar 44100 -y '{safe_filename(video.title)}.mp3'")
    #os.system(f"ffmpeg -i '{safe_filename(video.title)}.webm' -vn -ab 128k -ar 44100 -y '{safe_filename(video.title)}.mp3'")
    try:
        im = Image.open("picture.jpg")
        width, height = im.size   # Get dimensions
        left = (width - 500)/2
        top = (height - 500)/2
        right = (width + 500)/2
        bottom = (height + 500)/2

        # Crop the center of the image
        im = im.crop((left, top, right, bottom))
        #save resized image
        im.save('picture.jpg')
        audio = MP3(f"{safe_filename(video.title)}.mp3", ID3=ID3)
    except:
        await ytmp3.edit("**Sending mp3...**")
        await ytmp3.client.send_file(ytmp3.chat.id,
                              f'{safe_filename(video.title)}.mp3',
                              caption=f"{video.title}",
                              reply_to=reply_message, thumb='picture.jpg')
        return
    try:
        audio.add_tags()
    except error:
        pass
    audio.tags.add(APIC(mime='image/jpeg',type=3,desc=u'Cover',data=open('picture.jpg','rb').read()))
    audio.save()
    await yt.edit("**Sending mp3...**")
    msg_for_percentage = ytmp3
    await ytmp3.client.send_file(ytmp3.chat.id,
                              f'{safe_filename(video.title)}.mp3',
                              caption=f"{video.title}",
                              reply_to=reply_message, thumb='picture.jpg', progress_callback=callback)

    await ytmp3.delete()
    os.remove(f'{safe_filename(video.title)}.mp3')
    os.remove('picture.jpg')
    
async def callback(current, total):
    percent = round(current/total * 100, 2)
    await msg_for_percentage.edit(f"**Sending mp3...**\nUploaded `{current}` out of `{total}` bytes: `{percent}%`")

CMD_HELP.update({"ytmp3": ["YtMP3",
    " - `.ytmp3 (url)`: Convert a YouTube video to a mp3 and send it.\n"
                        ]})
