#!/bin/sh

filename="history.log"
maxsize=14500

while true
do
  filesize=$(ls -l "$filename" | awk '{print $5}')

  if ls /Volumes/ | grep -q Kindle
  then

    if [ $filesize -ge $maxsize ]
    then
      echo "[$(date)] Kindle connected, creating CSV file" > history.log
      echo "[$(date)] CSV created. Waiting for disconnect..." > history.log
    else
      echo "[$(date)] Kindle connected, creating CSV file" >> history.log
      echo "[$(date)] CSV created. Waiting for disconnect..." >> history.log
    fi

    python create_csv.py

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
      echo "[$(date)] Kindle not connected" > history.log
    else
      echo "[$(date)] Kindle not connected" >> history.log
    fi

  fi

  sleep 5
done
