# Quick Start Guide - G Train Display

## 🚀 For First-Time Setup

**Follow the comprehensive guide:** [`RASPBERRY_PI_SETUP.md`](RASPBERRY_PI_SETUP.md)

This will walk you through:
- Flashing the SD card
- Configuring WiFi
- Wiring the LCD
- Installing the software
- Setting up auto-start

⏱️ **Estimated time:** 2-3 hours

---

## 🔧 For Maintenance

### SSH into Your Pi

```bash
# If on same network as Pi
ssh pi@gtrain-display.local

# Or use IP address
ssh pi@192.168.1.XXX
```

### View Live Display Logs

```bash
sudo journalctl -u gtrain-display.service -f
```

Press `Ctrl+C` to stop viewing

### Restart the Display

```bash
sudo systemctl restart gtrain-display.service
```

### Stop the Display

```bash
sudo systemctl stop gtrain-display.service
```

### Start the Display

```bash
sudo systemctl start gtrain-display.service
```

### Check Display Status

```bash
sudo systemctl status gtrain-display.service
```

### Edit the Display Script

```bash
# Stop service first
sudo systemctl stop gtrain-display.service

# Edit script
nano ~/nyc-subway/display_train.py

# Save: Ctrl+X, Y, Enter

# Restart service
sudo systemctl start gtrain-display.service
```

### Update Display Settings

Common changes you might want to make in `display_train.py`:

```python
# Change refresh interval (line 19)
REFRESH_INTERVAL = 30  # Seconds between MTA data fetches

# Change how long each screen shows (line 20)
DISPLAY_INTERVAL = 4   # Seconds to show each direction

# Change LCD I2C address if needed (line 21)
LCD_ADDRESS = 0x27     # Try 0x3f if 0x27 doesn't work
```

After changes:
```bash
sudo systemctl restart gtrain-display.service
```

---

## 🏠 Moving to Different Location

1. **Unplug Pi** from power
2. **Transport to new location**
3. **Plug in power**
4. Pi will auto-connect if WiFi was pre-configured
5. Display starts automatically after ~60-90 seconds

### If WiFi Wasn't Pre-Configured

**Method 1: Use phone hotspot** with credentials you already set up

**Method 2: Update WiFi via SD card**
1. Power off Pi: `sudo shutdown -h now` (wait 30 seconds)
2. Remove SD card
3. Insert into laptop
4. Edit `wpa_supplicant.conf` on boot partition:

```bash
# Add new network
network={
    ssid="NewWiFiName"
    psk="NewWiFiPassword"
    priority=5
}
```

5. Eject, reinsert into Pi, power on

---

## 🐛 Troubleshooting

### LCD Shows Garbage or Nothing

```bash
# Check I2C connection
sudo i2cdetect -y 1

# Should show a number (27 or 3f)
# If nothing shows, check wiring

# If shows wrong address, update script
nano ~/nyc-subway/display_train.py
# Change LCD_ADDRESS value
```

### Display Shows "Network Error"

```bash
# Check WiFi
iwconfig

# Test internet
ping -c 4 google.com

# Check service logs
sudo journalctl -u gtrain-display.service -n 50
```

### Service Not Running

```bash
# Check status
sudo systemctl status gtrain-display.service

# Try starting
sudo systemctl start gtrain-display.service

# View errors
sudo journalctl -u gtrain-display.service -n 100
```

### Test Script Manually

```bash
cd ~/nyc-subway
source venv/bin/activate
python display_train.py

# Watch for errors
# Press Ctrl+C to stop
```

---

## 📊 Display Format

The 16x2 LCD alternates between two screens:

**Northbound (4 seconds):**
```
QUEENS       4 M
QUEENS      11 M
```

**Southbound (4 seconds):**
```
BROOKLYN     1 M
BROOKLYN    13 M
```

- Shows next 2 trains in each direction
- Minutes until arrival
- "NA" if no trains available
- Updates from MTA every 30 seconds

---

## 🔌 Hardware Connections

| LCD Pin | →  | Pi Zero Pin |
|---------|-----|-------------|
| VCC     | →  | Pin 2 (5V)  |
| GND     | →  | Pin 6 (GND) |
| SDA     | →  | Pin 3 (SDA) |
| SCL     | →  | Pin 5 (SCL) |

---

## 💡 Useful Commands

```bash
# Reboot Pi
sudo reboot

# Shutdown Pi (wait 30 sec before unplugging)
sudo shutdown -h now

# Check CPU temperature
vcgencmd measure_temp

# Check disk space
df -h

# Check memory usage
free -h

# Update system packages
sudo apt-get update
sudo apt-get upgrade

# View WiFi networks
sudo iwlist wlan0 scan | grep SSID
```

---

## 📝 Files Overview

- `display_train.py` - Main display script (runs on Pi)
- `read_g_train.py` - Simple test script (for Mac testing)
- `requirements.txt` - Python dependencies
- `RASPBERRY_PI_SETUP.md` - Complete setup guide
- `QUICK_START.md` - This file (quick reference)
- `scratchpad.md` - Project planning notes

---

## 🆘 Need Help?

1. Check service logs: `sudo journalctl -u gtrain-display.service -n 50`
2. Run script manually to see errors: `python display_train.py`
3. Check wiring and I2C: `sudo i2cdetect -y 1`
4. Review full setup guide: [`RASPBERRY_PI_SETUP.md`](RASPBERRY_PI_SETUP.md)

---

**Project:** NYC G Train Display  
**Station:** Greenpoint Avenue (G22)  
**MTA Data:** Real-time GTFS feed (updates every 30 seconds)

