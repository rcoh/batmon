# Batmon

Batmon is a simple Python script that monitors battery usage on Linux and sends desktop notifications when the battery is low. It's intended to improve the UX when using window managers like XMonad that don't bring all of gnome's conveniences. It uses `notify-send` to send notifications to the desktop.

## Usage
```
pip install batmon
```
Next, find your battery with `ls /sys/class/power_supply/`. Usually it's `BAT0`.
Then, in your `.xmonadrc` or similar, `batmon [BATTERY] &`. That's it!

