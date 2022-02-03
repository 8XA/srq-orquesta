___
<p align="center"><b>ACERCA DE</b></p>  

<p align="justify"><b>SRQ ORQUESTA</b> centraliza, dirige y facilita la interacción entre los elementos de software requeridos para el disfrute de una buena película/serie: Torrents, Subtítulos y Reproductor de video. El objetivo de este software es facilitar la reproducción de material de dominio público, libre de copyright y libre de publicidad. El uso que se le dé a SRQ ORQUESTA queda bajo la entera responsabilidad del usuario, dado que los resultados obtenidos mediante el mismo dependen directamente de plataformas externas sobre las cuales el desarrollador no tiene control.</p>  

<p align="center"><i>*Este software está diseñado para correr sobre <b>Android</b> utilizando <b>Termux v0.117</b>. Todas las características descritas en sus manuales son ya funcionales, sin embargo aún se encuentra en desarrollo.</i></p>

___

<p align="center"><b>Características destacables:</b></p>  

1. Búsqueda y reproducción de videos locales (Requiere un reproductor de videos externo).  
2. Busqueda y ejecución de Torrents de video (Requiere un cliente de descarga externo).  
3. Búsqueda y descarga de subtítulos.  
4. *Próximamente: Soporte para chromecast.*  

___

<p align="center"><b>Cómo instalar:</b></p>  

1. Descarga e instala el apk de [Termux v0.117](https://f-droid.org/repo/com.termux_117.apk).  
    * *Se adjunta el enlace de descarga desde su página oficial, dado que la versión disponible en Play Store es anterior a la requerida.*  
2. Copia el comando completo del siguiente [enlace](https://raw.githubusercontent.com/8XA/srq-orquesta/master/installation_commands.txt).  
3. Abre **Termux v0.117**, ingresa el comando copiado y da 'Enter'.
    * *Con esta acción comenzará la instalación*  
4. Durante el proceso de instalación ocurrirán los siguientes eventos que requieren la intervención del usuario:
    1. Al finalizar la primera etapa de la instalación se mostrará un mensaje sugiriendo la instalación complementaria de **LibreTorrent**. Al dar 'Enter' serás dirigido a Play Store. Puedes utilizar cualquier cliente Torrent, sin embargo **LibreTorrent** es muy completo, soporta descarga secuencial, tiene mayor integración con **SRQ ORQUESTA** y es libre. Al completar este paso, regresa a **Termux**.  
        * **Configuraciones de LibreTorrent recomendadas:**  
            * Acceso al almacenamiento: Permitir.  
            * Notificación de torrent finalizado: Deshabilitar.  
            * Solo conexiones sin límite: Habilitado.  
            * Salir después de finalizar todas las descargas: Habilitado.  
            * Mantener dispositivo despierto: Habilitado.  
            * Guardar torrents en:  
                > /storage/emulated/0/Download/Torrents  
            * Ejecutar una sola vez: Habilitado.  
            * Descarga secuencial (Aparece al momento de iniciar un torrent): Habilitado.  
    3. Tras la acción con el cliente 'Torrent', se mostrará un mensaje sugiriendo la instalación de **mpv-android**. Al dar 'Enter' serás dirigido a Play Store. Puedes utilizar cualquier otro reproductor de videos, sin embargo **mpv-android** soporta reproducción de subtítulos, integra códecs y es libre. Al completar este paso, regresa a **Termux**.  
        * **Configuraciones de mpv-android recomendadas**  
            * Acceso al almacenamiento: Permitir.  
            * Save position on quit: Habilitado.  
    5. Tras la acción con el reproductor de videos, se mostrará un mensaje relativo a la instalación de dependencias. Simplemente da 'Enter' y espera a que el proceso finalice e inicie **SRQ ORQUESTA**. 
        * **Acciones en SRQ ORQUESTA recomendadas**.
            * En su primera ejecución, **SRQ ORQUESTA** solicitará permiso de acceso al almacenamiento. Acepta.  
            * Tras iniciar, verás listados todos los videos del dispositivo. Cambia la ruta de exploración en la sección 'Carpeta', para ello ingresa 'c'.  
                * Ruta sugerida (Debe apuntar a la misma carpeta de descarga que el cliente Torrent):  
                    >'/sdcard/Download/Torrents'
            * Cada sección tiene su manual de ayuda, para acceder a él ingresa 'y'.  
  
---

<p align="center"><b>Ejemplo básico de uso:</b></p>  
  
La siguiente imagen es un enlace a YouTube, el video enlazado muestra de manera superficial el proceso de:  

1. Búsqueda y descarga de un Torrent.  
2. Selección local de la descarga.  
3. Subtitulado y reproducción de la película.  
  
[![](https://img.youtube.com/vi/ybCUnPuAA_Q/maxresdefault.jpg)](https://youtu.be/ybCUnPuAA_Q)


