import os

from pytube import YouTube
from pytube.helpers import safe_filename

from userbot import CMD_HELP
from userbot.events import register
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error

@register(outgoing=True, pattern=r"^\.ytmp3 (\S*)")
async def youtube_mp3(yt):
    reply_message = await yt.get_reply_message()
    url = yt.pattern_match.group(1)

    await yt.edit("**Processing...**")

    video = YouTube(url)
    stream = video.streams.filter(only_audio=True, mime_type="audio/webm").last()
    os.system(f"wget -q -O 'picture.jpg' {video.thumbnail_url}")
    await yt.edit("**Downloading audio...**")
    stream.download(filename=f'{safe_filename(video.title)}')
    await yt.edit("**Converting to mp3...**")
    os.system(f"ffmpeg -loglevel panic -i '{safe_filename(video.title)}.webm' -vn -ab 128k -ar 44100 -y '{safe_filename(video.title)}.mp3'")
    audio = MP3(f"{safe_filename(video.title)}.mp3", ID3=ID3)
    try:
        audio.add_tags()
    except error:
        pass
    audio.tags.add(APIC(mime='image/jpeg',type=3,desc=u'Cover',data=open('picture.jpg','rb').read()))
    audio.save()
    await yt.edit("**Sending mp3...**")
    await yt.client.send_file(yt.chat.id,
                              f'{safe_filename(video.title)}.mp3',
                              caption=f"{video.title}",
                              reply_to=reply_message, thumb='picture.jpg')

    await yt.delete()
    os.remove(f'{safe_filename(video.title)}.mp3')
    os.remove('picture.jpg')
    
CMD_HELP.update({"ytmp3": ["YtMP3",
    " - `.ytmp3 (url)`: Convert a YouTube video to a mp3 and send it.\n"
                        ]})
