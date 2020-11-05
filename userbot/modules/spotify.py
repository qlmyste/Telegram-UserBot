from asyncio import sleep
from json import loads
from json.decoder import JSONDecodeError
from os import environ
from sys import setrecursionlimit
import spotify_token as st
from time import gmtime, strftime
from requests import get
from requests.exceptions import HTTPError, ConnectionError
import telethon
from telethon.errors import AboutTooLongError, FloodWaitError
from telethon import errors
from telethon.tl.functions.account import UpdateProfileRequest
from youtube_search import YoutubeSearch
from moviepy import editor as mp
from pytube import YouTube
from pytube.helpers import safe_filename

from userbot import (BIO_PREFIX, BOTLOG, BOTLOG_CHATID, CMD_HELP, DEFAULT_BIO,
                     SPOTIFY_KEY, SPOTIFY_DC, bot)
from userbot.events import register

# =================== CONSTANT ===================
SPO_BIO_ENABLED = "`Spotify current music to bio has been successfully enabled.`"
SPO_BIO_DISABLED = "`Spotify current music to bio has been disabled. `"
SPO_BIO_DISABLED += "`Bio reverted to default.`"
SPO_BIO_RUNNING = "`Spotify current music to bio is already running.`"
ERROR_MSG = "`Spotify module halted, got an unexpected error.`"

artist = str
song = str

BIOPREFIX = BIO_PREFIX

SPOTIFYCHECK = False
RUNNING = False
OLDEXCEPT = False
PARSE = False
oldartist = ""
oldsong = ""
isWritedPause = False
isWritedPlay = False
isGetted = False
isDefault = True
isArtist = True
# ================================================
async def get_spotify_token():
    try:
      sptoken = st.start_session(SPOTIFY_DC, SPOTIFY_KEY)
    except HTTPError:
      await sleep(1)
      await get_spotify_token()
    access_token = sptoken[0]
    environ["spftoken"] = access_token


async def update_spotify_info():
    global artist
    global song
    global PARSE
    global SPOTIFYCHECK
    global RUNNING
    global OLDEXCEPT
    global isPlaying
    global isLocal
    global isArtist
    global isWritedPause
    global isWritedPlay
    global oldartist
    global oldsong
    global errorcheck
    global isGetted
    global data
    global isDefault
    spobio = ""

    while SPOTIFYCHECK:
        isGetted = False
        
        if isDefault == True:
          oldsong = ""
          oldartist = ""


        try:
            date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            RUNNING = True
            spftoken = environ.get("spftoken", None)
            hed = {'Authorization': 'Bearer ' + spftoken}
            url = 'https://api.spotify.com/v1/me/player/currently-playing'
            try:
                response = get(url,headers=hed)
                #print(str(response.status_code))
                if(response.status_code == 200):
                  data = loads(response.content)
                  isGetted = True
                  #print("SPOTIFY: response = " + str(response.status_code))
                elif response.status_code == 401: #No token provided
                  #print("SP: 401: " + response.reason)
                  await get_spotify_token()
                  await dirtyfix()
                else:
                  if isDefault == False:
                    await bot(UpdateProfileRequest(about=DEFAULT_BIO))
                    #print("SP: not 200 response, setting default.")
                    isDefault = True
            except Exception as e:
                isGetted = False
                print("SP: skip, exception:" + str(e))
                pass #skip
            if isGetted:
              isLocal = data['item']['is_local']
              isPlaying = data['is_playing']
              if isLocal:
                try:
                  artist = data['item']['artists'][0]['name']
                  song = data['item']['name']
                  if artist == "":
                    isArtist = False
                  else:
                    isArtist = True
                except IndexError:
                  song = data['item']['name']
                  artist = ""
                  isArtist = False
              else:
                  artist = data['item']['album']['artists'][0]['name']
                  song = data['item']['name']

              if isWritedPlay and isPlaying == False:
                isWritedPlay = False
              if isWritedPause and isPlaying == True:
                isWritedPause = False
              if (song != oldsong or artist != oldartist) or (isWritedPlay == False and isWritedPause == False):
                  oldartist = artist
                  oldsong = song
                  if isLocal:
                    if isArtist:
                      spobio = BIOPREFIX + " 🎧: " + artist + " - " + song + " [LOCAL]"
                    else:
                      spobio = BIOPREFIX + " 🎧: " + song + " [LOCAL]"
                  else:
                    spobio = BIOPREFIX + " 🎧: " + artist + " - " + song
                  if isPlaying == False:
                    spobio += " [PAUSED]"
                    isWritedPause = True
                  elif isPlaying == True:
                    isWritedPlay = True
                  try:
                      await sleep(5)
                      await bot(UpdateProfileRequest(about=spobio))
                      isDefault = False
                  except AboutTooLongError:
                      try:
                        short_bio = "🎧: " + song
                        await sleep(5) #anti flood
                        await bot(UpdateProfileRequest(about=short_bio))
                        isDefault = False
                      except AboutTooLongError:
                        short_bio = "🎧: " + song
                        await sleep(5) #anti flood
                        symbols = 0
                        for i in range(len(short_bio)):
                          symbols = symbols + 1
                        if symbols > 70:
                          short_bio = short_bio[:67]
                          short_bio += '...'
                        await bot(UpdateProfileRequest(about=short_bio))
                        isDefault = False
                  errorcheck = 0
                  OLDEXCEPT = False
            else: #means no new data. NO need to update. Trying to get again by new loop 
              #print("no new data, trying again")
              pass
        except KeyError:   #long pause
                #print("keyerror: " + date)
                if errorcheck == 0:
                  await update_token()
                elif errorcheck == 1:
                  if OLDEXCEPT == False:
                    await sleep(5) #anti flood
                    await bot(UpdateProfileRequest(about=DEFAULT_BIO))
                    isDefault = True
                  OLDEXCEPT = True
                  try:
                      await sleep(10)
                      await dirtyfix()
                  except errors.FloodWaitError as e:
                    await sleep(e.seconds)
                    await dirtyfix()
        except JSONDecodeError:   #NO INFO ABOUT, user closed spotify client
            #print("JSONDecodeError")
            if OLDEXCEPT == False:
              await sleep(5) #anti flood
              await bot(UpdateProfileRequest(about=DEFAULT_BIO))
              isDefault = True
            OLDEXCEPT = True
            try:
                await sleep(10) #no need to ddos a spotify servers
                await dirtyfix()
            except errors.FloodWaitError as e:
                await sleep(e.seconds)
                await dirtyfix()
        except TypeError:
            #print("TypeError")
            await sleep(5)
            await bot(UpdateProfileRequest(about=DEFAULT_BIO))
            isDefault = True
            await dirtyfix()
        except IndexError:
            #print("IndexError")
            await sleep(5)
            await bot(UpdateProfileRequest(about=DEFAULT_BIO))
            isDefault = True
            await dirtyfix()
        except errors.FloodWaitError as e:
            #print("Telegram anti-flood: Need to wait " + str(e.seconds) + " seconds")
            await sleep(e.seconds)
            await bot(UpdateProfileRequest(about=DEFAULT_BIO))
            isDefault = True
            await dirtyfix()
        except HTTPError:
            #print("HTTPErr")
            await bot(UpdateProfileRequest(about=DEFAULT_BIO))
            isDefault = True
            await dirtyfix()

        SPOTIFYCHECK = False
        await sleep(5)
        await dirtyfix()
    RUNNING = False


async def update_token():
    try:
      sptoken = st.start_session(SPOTIFY_DC, SPOTIFY_KEY)
    except HTTPError:
      await sleep(1)
      await update_token()
    except:
      print("Can't get sp token. The token is likely expired")
    access_token = sptoken[0]
    environ["spftoken"] = access_token
    errorcheck = 1
    await update_spotify_info()


async def dirtyfix():
    global SPOTIFYCHECK
    SPOTIFYCHECK = True
    await sleep(5)
    await update_spotify_info()


@register(outgoing=True, pattern="^.spoton$")
async def set_biostgraph(setstbio):
    setrecursionlimit(700000)
    if not SPOTIFYCHECK:
        environ["errorcheck"] = "0"
        await setstbio.edit(SPO_BIO_ENABLED)
        await get_spotify_token()
        await dirtyfix()
    else:
        await setstbio.edit(SPO_BIO_RUNNING)


@register(outgoing=True, pattern="^.spotoff$")
async def set_biodgraph(setdbio):
    global SPOTIFYCHECK
    global RUNNING
    SPOTIFYCHECK = False
    RUNNING = False
    await bot(UpdateProfileRequest(about=DEFAULT_BIO))
    await setdbio.edit(SPO_BIO_DISABLED)
    
@register(outgoing=True, pattern="^.song")
async def show_song(song_info):
        global isArtist
        global artist
        global song
        global isGetted
        await find_song()
        str_song = "Now playing: "
        if isGetted:
          if isArtist:
            str_song += '`' + artist + " - " + song + '`'
          else:
            str_song += '`' + song + '`'
          if link != '':
            str_song += f"\n**Spotify link:** {link}"
          await song_info.edit(str_song)
        else:
          await song_info.edit("Can't find current song in spotify")
          return
        
        #yt link
        song_author_str = author + ' - ' + song
        if isGetted:
          results = YoutubeSearch(song_author_str, max_results=1).to_json()
          try:
            data = loads(results)
          except JSONDecodeError:
            print("JSONDecode Error. Can't get yt link.")
            str_song += "\n\n Youtube: `JSONDecode Error. Can't found.`"
            await song_info.edit(str_song)
            return
          except:
            str_song += "\n\n Youtube: `Unexcepted Error. Can't found.`"
            await song_info.edit(str_song)
            return
          finally:
            str_song += "\n\nFound song link for: " + data['videos'][0]['title']
            str_song += "\nYoutube: https://youtube.com" + data['videos'][0]['url_suffix']
            await song_info.edit(str_song)
            return

@register(outgoing=True, pattern="^.spdl$")
async def sp_download(spdl):
  reply_message = await yt.get_reply_message()
  global song
  global artist
  await find_song()
  if isGetted:
    str_song_artist = artist + " - " + song
    results = YoutubeSearch(song_author_str, max_results=1).to_json()
    try:
      data = loads(results)
    except JSONDecodeError:
      await spdl.edit("JSONDecodeError. Can't found in yt.")
    except:
      await spdl.edit("Something went wrong. :(")
    finally:
      link = "https://youtube.com" + data['videos'][0]['url_suffix']
      spdl.edit("**Processing...**")
      video = YouTube(url)
      stream = video.streams.filter(progressive=True, subtype="mp4").first()
      await spdl.edit("**Downloading video...**")
      stream.download(filename='video')
      await spdl.edit("**Converting video...**")
      clip = mp.VideoFileClip('video.mp4')
      clip.audio.write_audiofile(f'{safe_filename(video.title)}.mp3')
      await spdl.edit("**Sending mp3...**")
      await spdl.client.send_file(spdl.chat.id,
                              f'{safe_filename(video.title)}.mp3',
                              caption=f"{video.title}",
                              reply_to=reply_message)
async def find_song():
        global isArtist
        global artist
        global song
        global isGetted
        isGetted = False
        await get_spotify_token()
        spftoken = environ.get("spftoken", None)
        hed = {'Authorization': 'Bearer ' + spftoken}
        url = 'https://api.spotify.com/v1/me/player/currently-playing'
        try:
          response = get(url,headers=hed)
        except:
          await song_info.edit("Something went wrong. Trying again...")
          try:
            await sleep(1)
            response = get(url,headers=hed)
          except:
            await song_info.edit("Can't connect to spotify servers.")
            return
        #print(str(response.status_code))
        if(response.status_code == 200):
          #print("SPOTIFY: response = " + str(response.status_code))
          data = loads(response.content)
          isLocal = data['item']['is_local']
          if data['item']['artists'][0]['name'] == "":
            isArtist = False
          if isLocal:
            artist = data['item']['artists'][0]['name']
            song = data['item']['name']
            isGetted = True
          else:
              artist = data['item']['album']['artists'][0]['name']
              song = data['item']['name']
              isGetted = True
        else:
          isGetted = False

CMD_HELP.update({"spotify": ['Spotify',
    " - `.spoton`: Enable Spotify bio updating.\n"
    " - `.spotoff`: Disable Spotify bio updating.\n"
    " - `.spdl`: Find current spotify song in youtube and download it!.\n"
    " - `.song:`: Show current playing song.\n"]
})
