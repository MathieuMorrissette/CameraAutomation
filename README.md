# CameraAutomation
Script to disables my home camera when I'm home
```
export VISUAL=nano; crontab -e
* * * * * /usr/bin/python3 /home/alarm/cron_scripts/CameraAutomation/smartplug-control.py
```
