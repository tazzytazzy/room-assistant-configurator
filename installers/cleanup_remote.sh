#!/usr/bin/env bash

if [ $# -eq 0 ]
  then
    echo "No arguments supplied. Put remote IP/Host as argument 1."
    exit
fi

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
TOOLPATH="$(dirname "$SCRIPTPATH")"

ssh pi@$1 "rm -rf /home/pi/room-assistant/installers && rm -rf /home/pi/room-assistant/src"
