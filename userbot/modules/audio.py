import os, json, requests, time
from userbot import BOTLOG, bot, BOTLOG_CHATID, CMD_HELP
from userbot.events import register
from userbot import AUDIOTAG_API as API_CODE

api_url = 'https://audiotag.info/api'

@register(outgoing=True, pattern=r"^\.audio$")
async def audiotag(at):
  if API_CODE is None:
    await at.edit("**We don't support magic! No API Code! Take it from audiotag.info**")
    return
  message = await at.get_reply_message()
  if message.audio or message.voice:
    file = message.audio or message.voice
    await at.edit("**Getted audio file**")
    await at.edit("**Downloading**")
    file = await bot.download_file(file, "audio.mp3")
    await at.edit("**Downloaded**")
    await at.edit("**Converting**")
    os.system("ffmpeg -i audio.mp3 -ar 8000 -ac 1 -vn converted.wav")
    await at.edit("**Converted**")
    payload = {'action': 'identify', 'apikey': API_CODE}
    await at.edit("**Payload complete**")
    result = requests.post(api_url,data=payload,files={'file': open('converted.wav', 'rb')})
    await at.edit("**Result getted**")
    await at.edit(result.text)
    result_object = json.loads(result.text)
    if result_object['success']==True and result_object['job_status']=='wait':
      token = result_object['token'];
      n=1;
      job_status = 'wait';
      while n < 100 and job_status=='wait':
        time.sleep(0.5);
        n+=1;
        payload = {'action': 'get_result', 'token':token, 'apikey': API_CODE}
        result = requests.post(api_url,data=payload)
        #await at.edit(result.text)
        result_object = json.loads(result.text);
        #await at.edit(result_object);
        if 'success' in result_object and result_object['success']==True:
          job_status = result_object['result'];
        else:
          break;
      else:
        await at.edit("**Sorry, i can't recognize it.**")
  os.remove('converted.wav')
  os.remove('audio.mp3')
  pretty_print = json.dumps(result_object, indent=4, sort_keys=True)
  await at.edit(pretty_print)

  CMD_HELP.update({"audio": ["Audio",
    " - `.audio`: Reply to music or voice for identificating it with AudioTag.\n"]
})
