#!/bin/bash
python make_array_tweet.py $1
python append_tweetID.py $1
declare a=$1
declare -i num=0
declare str=append_$a
while read x; do
    php tweetid2json.php $x | python3 json_reader3.4.4.py $1
    num=$num+1
    echo $num
    sleep 6
done < $str
