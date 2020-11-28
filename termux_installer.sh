pkg update
pkg install -y libxml2 libxslt libjpeg* libjpeg-turbo redis postgresql libwebp poppler ffmpeg git python resolv-conf clang
pip install cffi
pip install -r requirements.txt 
pip install --upgrade --force-reinstall dnspython
sed -i 's:/etc/resolv.conf:/data/data/com.termux/files/usr/etc/resolv.conf:g' /data/data/com.termux/files/usr/lib/python3.8/site-packages/dns/resolver.py

#downloading grpcio, because most probably that installing from requirements are failed because of sources problem. Fixing now.
pip download grpcio -d grpcio
cd grpcio
tar -xf  grpcio*
cd $(ls -d */|head -n 1)
sed -i 's:-std=c++11 -std=gnu99: ' ./setup.py
echo "Now you must edit your config.env file and start it via ./init/start.sh"

