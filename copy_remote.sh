#!/usr/bin/env bash

if [ $# -eq 0 ]
  then
    echo "No arguments supplied. Put remote IP/Host as argument 1."
    exit
fi

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
TOOLPATH="$SCRIPTPATH"

rsync -a $TOOLPATH/src $TOOLPATH/installers pi@$1:/home/pi/room-assistant/

echo "Done. If there's no, errors, ssh to the peer, change the 'installers' directory and run './install_rpi_xxx.sh'"
