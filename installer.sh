#Instalador para Termux android

set -e
pkg install -y python
pkg install -y wget
pkg install -y iconv
pkg install -y unrar
pkg install -y p7zip
pkg install -y readline
pkg install -y file
pip install termcolor
pip install chardet
sed -i '1i exec python /data/data/com.termux/files/usr/share/apocalipsis-orquesta/apocalipsis-orquesta/start.py' /data/data/com.termux/files/usr/etc/bash.bashrc
echo "alias aoq='exec python /data/data/com.termux/files/usr/share/apocalipsis-orquesta/apocalipsis-orquesta/start.py'" >> "/data/data/com.termux/files/usr/etc/bash.bashrc"
clear
termux-setup-storage
echo "Instalación completa. Presiona Enter para salir e inicia Termux de nuevo."
read listo
