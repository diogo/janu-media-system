#!/bin/bash

TOKEN=$(curl system:system@localhost:5000/get_token/ 2>/dev/null | sed 's/"\(.*\)"/\1/g')
if [ "$1" = 'create' ]; then
    curl localhost:5000/mediasource/?token=$TOKEN -F name='janu_test' -F module_id='1' -F user='diogo.comp@gmail.com' -F password='ttnp4590!' -F appid='33344' -F apikey='9zgxll3p44ma1685bco6sthub2g8m6uv5mri0zc2'
elif [ "$1" = 'query' ]; then
    echo 'Users:'
    curl localhost:5000/user/?token=$TOKEN
    echo -e '\n\nMedia Sources:'
    curl localhost:5000/mediasource/?token=$TOKEN
    echo
elif [ "$1" = 'expire' ]; then
    curl localhost:5000/user/?token=$TOKEN
    sleep 12
    curl localhost:5000/user/?token=$TOKEN
elif [ "$1" = 'artists' ]; then
	curl "localhost:5000/artist/?token=$TOKEN&mediasources=$2"
elif [ "$1" = 'medias' ]; then
	curl "localhost:5000/artist/$2/media/?token=$TOKEN&mediasources=$3"
elif [ "$1" = 'medias_pl' ]; then
    curl "localhost:5000/playlist/$2/media/?token=$TOKEN&mediasources=$3"
elif [ "$1" = 'playlists' ]; then
    curl "localhost:5000/artist/$2/playlist/?token=$TOKEN&mediasources=$3"
elif [ "$1" = 'media' ]; then
    curl "localhost:5000/media/$2/?token=$TOKEN&mediasources=$3"
elif [ "$1" = 'delete' ]; then
	curl -X DELETE "localhost:5000/mediasource/$2/?token=$TOKEN"
elif [ "$1" = 'genres' ]; then
	curl "localhost:5000/genre/?token=$TOKEN&mediasources=$2"
elif [ "$1" = 'artists_gr' ]; then
	curl "localhost:5000/genre/$2/artist/?token=$TOKEN&mediasources=$3"
fi