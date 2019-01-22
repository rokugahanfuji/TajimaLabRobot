## Tajima Lab Robot

### How to Install

1. Run `install.sh`
   1. Type `sudo sh install.sh`

2. Check your Joy-Con ID and Connect it.
   1. Type `bluetoothctl`
   2. Type `scan on`
   3. Find your Joy-Con ID and memo it.
   4. Type `pair {YOUR JOYCON ID}`
   5. Type `trust {YOUR JOYCON ID}`
   6. Type `connect {YOUR JOYCON ID}`
   7. Type `quit`

3. Change DEVICE_ID in `TajimaLabRobot/Switch/SwitchRobot.py`
   1. Add your Joy-Con ID between double-quatations in 11 lines.
      - DEVICE_ID = "XX:XX:XX:XX:XX:XX:XX"`

4. Add `sh /home/pi/TajimaLabRobot/robot.sh &` to `/etc/rc.local`
   - It need to added begore `exit 0` 


