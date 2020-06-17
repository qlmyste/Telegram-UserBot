""" Userbot module for shortening links using kutt.it """

import requests

from userbot import KUTT_IT_API_KEY, CMD_HELP
from userbot.events import register
from userbot.utils import parse_arguments, extract_urls

API_ENDPOINT = "https://kutt.it/api/"


@register(outgoing=True, pattern=r"^\.kutt\s?([\S\s]+)?")
async def kutt_it(e):
    reply_message = await e.get_reply_message()
    params = e.pattern_match.group(1) or ""
    args, params = parse_arguments(params, ['reuse'])

    urls = extract_urls(params)
    urls.extend(extract_urls(reply_message.text or ""))

    print(urls)

    if not urls:
        await e.edit("Need a URL to convert", delete_in=3)
        return

    reuse = args.get('reuse', False)
    await e.edit("Kutting...")

    shortened = {}
    for url in urls:
        payload = {'target': url, 'reuse': reuse}
        headers = {'X-API-Key': KUTT_IT_API_KEY}
        resp = requests.post(API_ENDPOINT + "url/submit", json=payload, headers=headers)

        json = resp.json()
        if resp.status_code == 200:
            shortened[url] = json['shortUrl']
        else:
            shortened[url] = None

    message = ""
    for item in shortened.items():
        message += f"Original URL: {item[0]} \nShortened URL: {item[1]} \n"

    await e.edit(message, link_preview=False)

CMD_HELP.update({
    ".kutt":
    "Uses kutt.it to shorten links.\
    \nWith any number of URLs. All will be converted.\
    \n`.kutt [options] (url1) (url2) ... (urlN)`\
    \nOr, in response to a message containing URLs.\
    \n`.kutt [options]`\
    \n\nOptions:\
    \n`.reuse`: Allows previously converted URLs to be reused (default: `False`)"
})

CMD_HELP.update({"kutt": ["Kutt",
    " - `..kutt [options] (url1) (url2) ... (urlN)`: Uses kutt.it to shorten links. With any number of URLs. All will be converted. Or, in response to a message containing URLs.\n"
    " - `.kutt [options]`: Uses kutt.it to shorten links with options.\n"
    " - `reuse`: Option. Allows previously converted URLs to be reused (default: `False`)\n"]
})
