#!/usr/bin/env bash

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
TOOLPATH="$(dirname "$SCRIPTPATH")"

echo ""
echo ""
echo ""
echo "Completing room assistant installation."
echo ""
echo "Upgrading NPM."
sudo npm install -g npm@8.3.0
echo ""
echo ""
echo "Installing Room-Assistant. This can take a very long time slower devices, about 30 minutes."
echo ""
sudo npm i --global --unsafe-perm room-assistant
sudo setcap cap_net_raw+eip $(eval readlink -f `which node`)
sudo setcap cap_net_raw+eip $(eval readlink -f `which hcitool`)
sudo setcap cap_net_admin+eip $(eval readlink -f `which hciconfig`)

sudo systemctl enable room-assistant.service
#sudo systemctl start room-assistant.service

echo ""
echo ""
echo ""
echo ""
echo "Installation is complete. Service has been enabled, but not started. Service"
echo "will start on next reboot **OR** when configurations are pushed to device"
echo "using ./send_configs.py"
echo ""
echo "Don't worry if the service starts with no configurations, it won't do much."
echo ""
