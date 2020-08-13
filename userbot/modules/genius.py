#Developed by Oleh Polisan. get_args_split_by kanged from Friendly Telegram (https://gitlab.com/friendly-telegram/).
from userbot import BOTLOG, bot, BOTLOG_CHATID, CMD_HELP, GENIUS_API, SPOTIFY_KEY, SPOTIFY_DC
from userbot.events import register
from userbot.utils import get_args_split_by
import spotify_token as st
from requests import get
import lyricsgenius
from os import environ
from json import loads

genius = lyricsgenius.Genius(GENIUS_API)

@register(outgoing=True, pattern=r"^\.lyrics(.*)")
async def gen(e):
      if GENIUS_API is None:
        await e.edit("**We don't support magic! No Genius API!**")
        return
      args = get_args_split_by(e.pattern_match.group(), ",")
      if len(args) == 2:
            name = args[0]
            artist = args[1]
            await e.edit("**Searching for song **" + name + "** by **" + artist)
            song = genius.search_song(name, artist)
      else:
            await e.edit("**Trying to get Spotify lyrics...**")
            if SPOTIFY_KEY is None:
                  await e.edit("**Spotify cache KEY is missing**")
                  return
            if SPOTIFY_DC is None:
                  await e.edit("**Spotify cache DC is missing**")
                  return
            #getting spotify token
            sptoken = st.start_session(SPOTIFY_DC, SPOTIFY_KEY) 
            access_token = sptoken[0]
            environ["spftoken"] = access_token
            oldartist = ""
            oldsong = ""
            spftoken = environ.get("spftoken", None)
            hed = {'Authorization': 'Bearer ' + spftoken}
            url = 'https://api.spotify.com/v1/me/player/currently-playing'
            response = get(url, headers=hed)
            data = loads(response.content)
            artist = data['item']['album']['artists'][0]['name']
            name = data['item']['name']
            print(artist + " - " + name)
            await e.edit("**Searching for song **" + name + "** by **" + artist)
            song = genius.search_song(name, artist)
      if song is None:
        await e.edit("**Can't find song **" + name + "** by **" + artist)
        return
      await e.edit("**Lyrics for: **" + name + " - " + artist + " \n" + song.lyrics)
      
CMD_HELP.update({"lyrics": ["Lyrics",
    " - `.lyrics <song>, <author>`: Search lyrics in Genius platform\n"
    "You'll need an Genius api, which one you can get from https://genius.com/api-clients. \nIn APP WEBSITE URL type any url (such as http://example.com) and copy CLIENT ACCESS TOKEN to config.env file\n"
    " - `.lyrics`: Search lyrics of song played now in Spotify"]
})
