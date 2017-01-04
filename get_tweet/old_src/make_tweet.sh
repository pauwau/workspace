#!/bin/bash
declare -i num=0
while read x; do
    php tweetid2json.php $x | python3 json_reader3.4.4.py
    num=$num+1
    echo $num
    sleep 6
done < $1
