pkg update
pkg install -y libxml2 libxslt libjpeg* libjpeg-turbo redis postgresql libwebp poppler ffmpeg git python resolv-conf 
pip3 install -y bs4 spectra lottie cairosvg pytube3 pillow wakeonlan psutil ffmpeg moviepy spotify-token redis dnspython humanize pydrive wikipedia lxml search-engine-parser speedtest-cli telegraph telethon urbandict pytz requests googletrans gtts hachoir pybase64 aiohttp cowpy emoji gTTS-token gTTS gitpython google-api-python-client oauth2client google_images_download SQLAlchemy psycopg2-binary spectra google-cloud-speech google-cloud-texttospeech mutagen python-dotenv pydownload pylast pymongo Randomwords lyricsgenius convertapi pdf2image cairocffi
pip install --upgrade --force-reinstall dnspython
sed -i 's:/etc/resolv.conf:/data/data/com.termux/files/usr/etc/resolv.conf:g' /data/data/com.termux/files/usr/lib/python3.8/site-packages/dns/resolver.py
echo "Now you must edit your config.env file and start it via ./init/start.sh"

