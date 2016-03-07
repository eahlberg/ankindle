#!/bin/sh

filename="monitor.log"
maxsize=14500
csvfile="kindle_vocab.csv"
kindledb="/Volumes/Kindle/system/vocabulary/vocab.db"
api_key="API_KEY"

if [ ! -f "$filename" ]
then
  touch "$filename"
else
  :
fi

while true
do
  filesize=$(ls -l "$filename" | awk '{print $5}')

  if ls /Volumes/ | grep -q Kindle
  then

    if [ $filesize -ge $maxsize ]
    then
      echo "[$(date)] Kindle connected, creating CSV file" > monitor.log
      echo "[$(date)] CSV created. Waiting for disconnect..." > monitor.log
    else
      echo "[$(date)] Kindle connected, creating CSV file" >> monitor.log
      echo "[$(date)] CSV created. Waiting for disconnect..." >> monitor.log
    fi

    python main.py $csvfile $kindledb $api_key

    while true
    do
      if ! ls /Volumes/ | grep -q Kindle
      then
        break
      else
        :
      sleep 5
    fi
    done

  else
    if [ $filesize -ge $maxsize ]
    then
      echo "[$(date)] Kindle not connected" > monitor.log
    else
      echo "[$(date)] Kindle not connected" >> monitor.log
    fi

  fi

  sleep 5
done
