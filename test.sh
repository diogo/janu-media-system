#!/bin/bash

TOKEN=$(curl system:system@localhost:5000/get_token/ 2>/dev/null | sed 's/"\(.*\)"/\1/g')
if [ "$1" = 'create' ]; then
    curl localhost:5000/mediatype/?token=$TOKEN -F name=musicas
    curl localhost:5000/mediatype/?token=$TOKEN -F name=videos
    curl localhost:5000/mediatype/?token=$TOKEN -F name=fotos
    curl localhost:5000/mediatype/1/?token=$TOKEN -F name=musicas_sd -F module_id=1
    curl localhost:5000/mediatype/2/?token=$TOKEN -F name=videos_hd -F module_id=1
elif [ "$1" = 'query' ]; then
    echo 'Users:'
    curl localhost:5000/users/?token=$TOKEN
    echo -e '\n\nMedia Types:'
    curl localhost:5000/mediatypes/
    echo -e '\n\nMedia Sources:'
    curl localhost:5000/mediasources/
    echo
elif [ "$1" = 'expire' ]; then
    curl localhost:5000/users/?token=$TOKEN
    sleep 12
    curl localhost:5000/users/?token=$TOKEN
fi