#!/usr/bin/env bash

# This script is meant for devices that have more CPU, like
# RPI 3/4.  For RPI Zero, use install_rpi_slow.sh

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
TOOLPATH="$(dirname "$SCRIPTPATH")"

bash ./_install_common.sh $1

echo "Doing raspberry PI 3/4/etc 'node' install."
curl -sL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo cp ../src/service_rpi_fast /etc/systemd/system/room-assistant.service

echo ""
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""
echo "Done with first portion. Going to reboot now."
echo ""
echo "After reboot, type these commands to complete install:"
echo ""
echo "cd $(pwd)/installers"
echo "./install_finish.sh"
echo ""
sudo reboot
