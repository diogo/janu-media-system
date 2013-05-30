#!/bin/bash

TOKEN=$(curl system:system@localhost:5000/get_token/ 2>/dev/null | sed 's/"\(.*\)"/\1/g')
if [ "$1" = 'create' ]; then
    curl localhost:5000/mediasource/?token=$TOKEN -F name='janu_test' -F module_id='1' -F user='diogo.comp@gmail.com' -F password='ttnp4590!' -F appid='33344' -F apikey='9zgxll3p44ma1685bco6sthub2g8m6uv5mri0zc2'
elif [ "$1" = 'query' ]; then
    echo 'Users:'
    curl localhost:5000/users/?token=$TOKEN
    echo -e '\n\nMedia Sources:'
    curl localhost:5000/mediasources/
    echo
elif [ "$1" = 'expire' ]; then
    curl localhost:5000/users/?token=$TOKEN
    sleep 12
    curl localhost:5000/users/?token=$TOKEN
fi