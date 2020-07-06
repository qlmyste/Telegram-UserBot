FROM olegpolisan/tg_userbot
ENV PATH="/app/bin:$PATH"
WORKDIR /app
RUN git clone https://github.com/PolisanTheEasyNick/Telegram-UserBot.git -b master /app
RUN pip3 uninstall -y pytube3
RUN pip3 install pytube3 Randomwords lyricsgenius
#
# Copies session and config(if it exists)
#
COPY ./userbot.session ./google.json* ./config.env* ./client_secrets.json* ./secret.json* /app/
#
# Finalization
#
CMD ["bash","init/start.sh"]
