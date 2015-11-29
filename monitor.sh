#!/bin/sh

while true
do
  if ls /Volumes/ | grep Kindle
  then
    echo "Kindle connected, creating CSV file"
    python create_csv.py
    echo "CSV created"
    break
  else
    echo "Kindle not connected"
  fi

  sleep 5
done
