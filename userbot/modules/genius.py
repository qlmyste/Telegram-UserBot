#Developed by Oleh Polisan. get_args_split_by kanged from Friendly Telegram (https://gitlab.com/friendly-telegram/).
from userbot import BOTLOG, bot, BOTLOG_CHATID, CMD_HELP, GENIUS_API, SPOTIFY_KEY, SPOTIFY_DC
from userbot.events import register
from userbot.utils import get_args_split_by
import spotify_token as st
from requests import get
import lyricsgenius

@register(outgoing=True, pattern=r"^\.lyrics (.*)")
async def gen(e):
      genius = lyricsgenius.Genius(GENIUS_API)
      if GENIUS_API is None:
        await e.edit("**We don't support magic! No Genius API!**")
        return
      args = get_args_split_by(e.pattern_match.group(), ",")
      if len(args) == 2:
            await e.edit("**Searching for song **" + args[0] + "** by **" + args[1])
            song = genius.search_song(args[0], args[1])
      if len(args) == 0:
            if SPOTIFY_KEY is None:
                  e.edit("**Spotify cache KEY is missing**")
                  return
            if SPOTIFY_DC is None:
                  e.edit("**Spotify cache DC is missing**")
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
            song = data['item']['name']
      else:
            await e.edit("**Syntax Error**")
            return
      if song is None:
        await e.edit("**Can't find song **" + args[0] + "** by **" + args[1])
        return
      await e.edit("**Lyrics for: **" + args[1] + " - " + args[0] + " \n" + song.lyrics)
      
CMD_HELP.update({"lyrics": ["Lyrics",
    " - `.lyrics <song>, <author>`: Search lyrics in Genius platform\n"
    "You'll need an Genius api, which one you can get from https://genius.com/api-clients. \nIn APP WEBSITE URL type any url (such as http://example.com) and copy CLIENT ACCESS TOKEN to config.env file"]
})

        await e.edit("**Syntax Error**")
        return
