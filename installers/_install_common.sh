#!/usr/bin/env bash

echo "Setting up basic raspberry items..."
cd
echo "" >> .profile
echo 'PATH="$PATH:/opt/nodejs/bin"' >> .profile

#echo "" >> .profile
#echo "export NODE_APP_INSTANCE=DeviceName" >> .profile

sudo sh -c "echo \"alias pico='nano'\" >> /etc/profile.d/00aliases.sh"
sudo sh -c "echo \"alias ll='ls -la'\" >> /etc/profile.d/00aliases.sh"

echo "Updating system..."
sudo apt update && sudo apt upgrade -y
sudo apt install build-essential libavahi-compat-libdnssd-dev libsystemd-dev bluetooth libbluetooth-dev libudev-dev libcairo2-dev libpango1.0-dev libjpeg-dev libgif-dev librsvg2-dev bluez bluez-hcidump  git -y
