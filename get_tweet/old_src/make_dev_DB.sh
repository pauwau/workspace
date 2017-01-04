#!/bin/bash
while read x; do
    php tweetid2json.php $x | python3 dev_reader_json.py
    sleep 6
done < $1
