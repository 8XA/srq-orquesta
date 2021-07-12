#Instalador para Termux android

set -e
pkg install -y python
pkg install -y wget
pkg install -y iconv
pkg install -y unrar
pkg install -y p7zip
pkg install -y readline
#pkg install -y file
pip install termcolor
pip install chardet
echo "alias sub='exec python /data/data/com.termux/files/usr/share/sub4time/sub4time/sub.py'" >> "/data/data/com.termux/files/usr/etc/bash.bashrc"
clear
termux-setup-storage
echo "Instalación completa. Presiona Enter para salir e inicia Termux de nuevo."
read listo


/data/data/com.termux/files/usr/etc/bash.bashrc
