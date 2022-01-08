#!/usr/bin/env bash

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
TOOLPATH="$(dirname "$SCRIPTPATH")"

bash ./_install_common.sh

# This script is meant for devices that have less CPU, like
# RPI Zero.  For RPI 3/4, use install_rpi_fast.sh


echo "Doing raspberry PI zero 'node' install."
wget -O - https://gist.githubusercontent.com/mKeRix/88b7b81e9bca044f74de1dc51696efb2/raw/799a20bca44cc61d8f8ae93878f2f28af8365a69/getNodeLTS.sh | sudo bash
sudo cp ../src/service_rpi_slow /etc/systemd/system/room-assistant.service

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
