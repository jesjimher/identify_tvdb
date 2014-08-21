identify_tvdb
=============

identify_tvdb es una pequeña utilidad que busca en thetvdb.com información sobre un fichero de vídeo, y lo renombra incluyendo información sobre temporada, número de capítulo, etc. El uso es muy sencillo:

    identify_tvdb.py -n "Nombre de la serie" fichero(s)

Por ejemplo, el siguiente comando:

    identify_tvdb.py -n "Lost" lost.s01e03.x264.mkv
    
Renombraría el fichero "lost.s01e03.x264.mkv" a "Lost - S01E03 - Tabula Rasa.mkv".

Adicionalmente, se puede indicar un idioma concreto con el parámetro "-l". Ejecutar con la opción -h para ver todas las opciones.

identify_tvdb no requiere de librerías demasiado sofisticadas. Sólo usa dos un poco especiales:

- tvdb_api: Para acceder y consultar thetvdb.com
- fuzzywuzzy: Para hacer búsquedas y encontrar los episodios

Las dos se pueden instalar fácilmente desde los repositorios de Ubuntu (o equivalente), o con "pip install XXX".
