from asyncio import sleep
from json import loads
from json.decoder import JSONDecodeError
from os import environ
from sys import setrecursionlimit
import spotify_token as st
from time import gmtime, strftime
from requests import get
import telethon
from telethon.errors import AboutTooLongError, FloodWaitError
from telethon import errors
from telethon.tl.functions.account import UpdateProfileRequest

from userbot import (BIO_PREFIX, BOTLOG, BOTLOG_CHATID, CMD_HELP, DEFAULT_BIO,
                     SPOTIFY_KEY, SPOTIFY_DC, bot, SPOTIFY_AUTO)
from userbot.events import register

# =================== CONSTANT ===================
SPO_BIO_ENABLED = "`Spotify current music to bio is now enabled.`"
SPO_BIO_DISABLED = "`Spotify current music to bio is now disabled. "
SPO_BIO_DISABLED += "Bio reverted to default.`"
SPO_BIO_RUNNING = "`Spotify current music to bio is already running.`"
ERROR_MSG = "`Spotify module halted, got an unexpected error.`"

ARTIST = 0
SONG = 0

BIOPREFIX = BIO_PREFIX

SPOTIFYCHECK = False
RUNNING = False
OLDEXCEPT = False
PARSE = False
oldartist = ""
oldsong = ""
isWritedPause = False
isWritedPlay = False


# ================================================
async def get_spotify_token():
    sptoken = st.start_session(SPOTIFY_DC, SPOTIFY_KEY)
    access_token = sptoken[0]
    environ["spftoken"] = access_token


async def update_spotify_info():
    global ARTIST
    global SONG
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
    spobio = ""
    
    while SPOTIFYCHECK:
        date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        try:
            RUNNING = True
            spftoken = environ.get("spftoken", None)
            hed = {'Authorization': 'Bearer ' + spftoken}
            url = 'https://api.spotify.com/v1/me/player/currently-playing'
            response = get(url, headers=hed)
            data = loads(response.content)
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
                except AboutTooLongError:
                    try:
                      short_bio = "🎧: " + song
                      await sleep(5) #anti flood
                      await bot(UpdateProfileRequest(about=short_bio))
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
                errorcheck = 0
                OLDEXCEPT = False
                
        except KeyError:   #long pause
                print("keyerror: " + date)
                if errorcheck == 0:
                  await update_token()
                elif errorcheck == 1:
                  if OLDEXCEPT == False:
                    await sleep(5) #anti flood
                    await bot(UpdateProfileRequest(about=DEFAULT_BIO))
                  OLDEXCEPT = True
                  try:
                      await sleep(10)
                      await dirtyfix()
                  except errors.FloodWaitError as e:
                    await sleep(e.seconds)
                    await dirtyfix()
        except JSONDecodeError:   #NO INFO ABOUT, user closed spotify client
            if OLDEXCEPT == False:
              await sleep(5) #anti flood
              await bot(UpdateProfileRequest(about=DEFAULT_BIO))
            OLDEXCEPT = True
            try:
                await sleep(10) #no need to ddos a spotify servers
                await dirtyfix()
            except errors.FloodWaitError as e:
                await sleep(e.seconds)
                await dirtyfix()
        except TypeError:
            await sleep(5)
            await dirtyfix()
        except IndexError:
            await sleep(5)
            await dirtyfix()
        except errors.FloodWaitError as e:
            print("def: Need to wait " + str(e.seconds) + " seconds")
            await sleep(e.seconds)
            await dirtyfix()
        except requests.exceptions.HTTPError:
            await dirtyfix()

        SPOTIFYCHECK = False
        await sleep(5)
        await dirtyfix()
    RUNNING = False


async def update_token():
    sptoken = st.start_session(SPOTIFY_DC, SPOTIFY_KEY)
    access_token = sptoken[0]
    environ["spftoken"] = access_token
    errorcheck = 1
    await update_spotify_info()


async def dirtyfix():
    global SPOTIFYCHECK
    SPOTIFYCHECK = True
    await sleep(5)
    await update_spotify_info()


@register(outgoing=True, pattern="^.enablespotify$")
async def set_biostgraph(setstbio):
    setrecursionlimit(700000)
    if not SPOTIFYCHECK:
        environ["errorcheck"] = "0"
        await setstbio.edit(SPO_BIO_ENABLED)
        await get_spotify_token()
        await dirtyfix()
    else:
        await setstbio.edit(SPO_BIO_RUNNING)


@register(outgoing=True, pattern="^.disablespotify$")
async def set_biodgraph(setdbio):
    global SPOTIFYCHECK
    global RUNNING
    SPOTIFYCHECK = False
    RUNNING = False
    await bot(UpdateProfileRequest(about=DEFAULT_BIO))
    await setdbio.edit(SPO_BIO_DISABLED)

if SPOTIFY_AUTO:
  SPOTIFYCHECK = True
  dirtyfix()
    
CMD_HELP.update({"spotify": ['Spotify',
    " - `.enablespotify`: Enable Spotify bio updating.\n"
    " - `.disablespotify`: Disable Spotify bio updating.\n"]
})
