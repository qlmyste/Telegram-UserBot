pkg update
pkg install -y libxml2 libxslt libjpeg* libjpeg-turbo redis postgresql libwebp poppler ffmpeg git python resolv-conf clang
pip install cffi
pip install -r requirements.txt
pip install --upgrade --force-reinstall dnspython
sed -i 's:/etc/resolv.conf:/data/data/com.termux/files/usr/etc/resolv.conf:g' /data/data/com.termux/files/usr/lib/python3.8/site-packages/dns/resolver.py

#export REPO_ROOT=grpc
#git clone https://github.com/grpc/grpc $REPO_ROOT
#cd $REPO_ROOT
#git submodule update --init
#pip install -r requirements.txt
#detele std=..
#sed -i 's:-std=gnu99: ' /data/data/com.termux/files/root/Telegram-UserBot/$REPO_ROOT/setup.py
#GRPC_PYTHON_BUILD_WITH_CYTHON=1 pip install .
echo "Now you must edit your config.env file and start it via ./init/start.sh"

