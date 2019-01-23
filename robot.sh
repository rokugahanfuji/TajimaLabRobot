#!/bin/sh
cd `dirname $0`

sudo python Switch/SwitchRobot.py

if [ $? = 0 ]; then
  sleep 5
  sudo shutdown now
fi
