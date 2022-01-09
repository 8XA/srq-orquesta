#Installer for termux in android

set -e
pkg install -y python


sed -i '1i exec python /data/data/com.termux/files/usr/share/srq-orquesta/srq-orquesta/start.py' /data/data/com.termux/files/usr/etc/bash.bashrc
echo "alias srq='exec python /data/data/com.termux/files/usr/share/srq-orquesta/srq-orquesta/start.py'" >> "/data/data/com.termux/files/usr/etc/bash.bashrc"
clear

echo "SRQ ORQUESTA recomienda 'LibreTorrent' como cliente de descargas (es libre y soporta la descarga secuencial). Aunque puedes usar cualquier otro. Presiona Enter para abrirlo en la Play Store: "
read
xdg-open "https://play.google.com/store/apps/details?id=org.proninyaroslav.libretorrent"

echo

echo "SRQ ORQUESTA recomienda 'mpv-android' como reproductor de videos (es libre, integra códecs y soporta subtítulos). Aunque puedes usar cualquier otro. Presiona Enter para abrirlo en la Play Store: "
read
xdg-open "https://play.google.com/store/apps/details?id=is.xyz.mpv"

clear
echo "Para iniciar la instalación de dependencias, presiona Enter: "
read

python /data/data/com.termux/files/usr/share/srq-orquesta/srq-orquesta/start.py
