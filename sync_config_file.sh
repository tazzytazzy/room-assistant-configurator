#!/usr/bin/env bash

if [ $# -eq 0 ]
  then
    echo "Put device name for argument 1, and IP/Host for argument 2"
    exit
fi

# Helper script for send_configs.py to deliver a config to a room assistant node.

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
TOOLPATH="$SCRIPTPATH"

if [ $# -ne 2 ]
  then
    echo "Command requires to params: <configname> <ip address>"
    exit
fi

rsync -a -q --rsync-path="mkdir -p ~/room-assistant/config && rsync" -v $TOOLPATH/dist/$1.yml pi@$2:~/room-assistant/config/local.yml
