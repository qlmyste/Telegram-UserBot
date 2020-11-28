pkg update
pkg install -y libxml2 libxslt libjpeg* libjpeg-turbo redis postgresql libwebp poppler ffmpeg git python resolv-conf clang
pip install cffi
pip install -r requirements.txt
pip install --upgrade --force-reinstall dnspython
sed -i 's:/etc/resolv.conf:/data/data/com.termux/files/usr/etc/resolv.conf:g' /data/data/com.termux/files/usr/lib/python3.8/site-packages/dns/resolver.py
echo "Now you must edit your config.env file and start it via ./init/start.sh"

