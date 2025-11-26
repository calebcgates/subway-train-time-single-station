# NYC G Train Display - Raspberry Pi Project Scratchpad

## Project Overview
Display real-time G train arrivals at Greenpoint Avenue on a 16x2 I2C LCD, alternating between northbound and southbound trains every 4 seconds.

## Display Format

### Northbound Screen (4 seconds)
```
QUEENS       4 M
QUEENS      11 M
```

### Southbound Screen (4 seconds)
```
BROOKLYN     1 M
BROOKLYN    13 M
```

## Hardware Requirements

### Components Needed
- [ ] Raspberry Pi Zero W (W model has WiFi built-in)
- [ ] 16x2 I2C LCD Display (typically with PCF8574 I2C backpack)
- [ ] MicroSD card (8GB+ recommended)
- [ ] Power supply (5V 2.5A micro USB)
- [ ] 4 female-to-female jumper wires (for I2C connection)

### I2C LCD Connection to Raspberry Pi Zero

#### Pin Connections
```
LCD Display    →    Raspberry Pi Zero
-----------------------------------------
VCC (5V)       →    Pin 2 or 4 (5V)
GND            →    Pin 6, 9, 14, 20, 25, 30, 34, or 39 (GND)
SDA            →    Pin 3 (GPIO 2 - SDA)
SCL            →    Pin 5 (GPIO 3 - SCL)
```

#### Pi Zero Pinout Reference
```
    3.3V  [ 1] [ 2]  5V     ← VCC here
     SDA  [ 3] [ 4]  5V
     SCL  [ 5] [ 6]  GND    ← GND here
         ...
```

## Software Requirements

### Python Libraries to Install
```bash
# I2C LCD libraries (need to determine which one - see questions below)
pip install RPLCD
# OR
pip install smbus2

# Existing requirements
pip install gtfs-realtime-bindings protobuf
```

### System Configuration
```bash
# Enable I2C interface on Raspberry Pi
sudo raspi-config
# Navigate to: Interface Options → I2C → Enable

# Install I2C tools
sudo apt-get update
sudo apt-get install -y i2c-tools python3-smbus

# Test I2C connection (after wiring)
sudo i2cdetect -y 1
# Should show address like 0x27 or 0x3f
```

## Code Modifications Needed

### Modified Script Features
1. Filter and sort trains:
   - Get next 2 northbound trains (sorted by arrival time)
   - Get next 2 southbound trains (sorted by arrival time)
2. Format for 16-character display
3. Alternate display every 4 seconds
4. Error handling for network issues
5. Continuous loop with refresh interval

### Display Format Notes
```
Position:     0123456789012345
Line 1:       BROOKLYN     1 M
Line 2:       BROOKLYN    13 M
              ^        ^    ^
              |        |    Right-aligned minutes
              |        Space padding
              Direction label
```

## WiFi Setup Options

### Option 1: Pre-configure WiFi (RECOMMENDED)
**Before taking Pi to other house:**
1. Edit `/boot/wpa_supplicant.conf` file on SD card
2. Add both home and destination WiFi credentials
3. Pi will auto-connect when powered on

```bash
# File: /boot/wpa_supplicant.conf
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="HomeWiFi"
    psk="HomePassword"
    priority=1
}

network={
    ssid="OtherHouseWiFi"
    psk="OtherHousePassword"
    priority=2
}
```

### Option 2: WiFi via Phone Hotspot
1. Set up a mobile hotspot with known credentials
2. Pre-configure Pi with hotspot credentials
3. Use hotspot to SSH in and configure new WiFi
4. Switch back to house WiFi

### Option 3: Headless WiFi Setup via SD Card
1. Power off Pi
2. Remove SD card
3. Insert into laptop
4. Edit wpa_supplicant.conf on boot partition
5. Reinsert and power on

## Auto-Start on Boot

### Method 1: systemd Service (RECOMMENDED)
```bash
# Create service file
sudo nano /etc/systemd/system/g-train-display.service
```

```ini
[Unit]
Description=G Train Display Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/nyc-subway
ExecStart=/home/pi/nyc-subway/venv/bin/python /home/pi/nyc-subway/display_train.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable g-train-display.service
sudo systemctl start g-train-display.service

# Check status
sudo systemctl status g-train-display.service
```

### Method 2: crontab
```bash
crontab -e

# Add line:
@reboot sleep 30 && cd /home/pi/nyc-subway && /home/pi/nyc-subway/venv/bin/python display_train.py
```

## Installation Steps Timeline

### Phase 1: Local Development (On your Mac)
- [x] Create and test basic train fetching script
- [ ] Modify script to filter 2+2 trains
- [ ] Add display logic (can test with print statements)
- [ ] Test alternating display logic

### Phase 2: Initial Raspberry Pi Setup (At current location)
- [ ] Flash Raspberry Pi OS Lite to SD card
- [ ] Enable SSH (add empty `ssh` file to boot partition)
- [ ] Configure WiFi for BOTH locations in wpa_supplicant.conf
- [ ] Boot Pi and connect via SSH
- [ ] Update system: `sudo apt-get update && sudo apt-get upgrade`
- [ ] Install Python dependencies
- [ ] Enable I2C interface
- [ ] Wire up LCD display
- [ ] Test I2C connection
- [ ] Transfer and test display script
- [ ] Configure autostart
- [ ] Test full system

### Phase 3: Deployment (At other house)
- [ ] Power on Pi (should auto-connect to WiFi)
- [ ] Display should start automatically
- [ ] Optional: SSH in to verify status

## Testing Checklist

### Local Testing (Mac)
- [ ] Script fetches train data
- [ ] Filters 2 northbound + 2 southbound
- [ ] Sorts by arrival time
- [ ] Formats strings correctly (16 chars)
- [ ] Handles missing/delayed trains gracefully

### Raspberry Pi Testing
- [ ] I2C device detected
- [ ] LCD displays text correctly
- [ ] Train data displays correctly
- [ ] Screen alternates every 4 seconds
- [ ] Handles network disconnection
- [ ] Starts automatically on boot
- [ ] Recovers from errors

## Confirmed Configuration ✅

### Hardware Specific
1. **LCD Model**: 16x2 I2C LCD with PCF8574T chip ✅
2. **LCD Address**: Will detect (typically 0x27 or 0x3f for PCF8574T) ✅
3. **Pi Model**: Raspberry Pi Zero W (with WiFi built-in) ✅
4. **Power**: 5V 2.5A micro USB power supply needed ✅

### WiFi Configuration
5. **WiFi Credentials**: Known - will store in .env file ✅
6. **Remote Access**: SSH access enabled with SSH key for debugging ✅

### Display Preferences
8. **Refresh Rate**: Fetch new data every 30 seconds ✅
9. **No Trains**: Display "NA" when no trains available ✅
10. **Direction Names**: "QUEENS" (northbound) and "BROOKLYN" (southbound) ✅
11. **Screen Rotation**: Alternate every 4 seconds between directions ✅

## Estimated Timeline

- Script modification: 30 minutes
- Raspberry Pi initial setup: 1-2 hours
- LCD wiring and testing: 30 minutes
- Troubleshooting and refinement: 1 hour
- **Total: 3-4 hours**

## Useful Commands Reference

```bash
# Check I2C devices
sudo i2cdetect -y 1

# View service logs
sudo journalctl -u g-train-display.service -f

# Stop/start service
sudo systemctl stop g-train-display.service
sudo systemctl start g-train-display.service

# Check WiFi status
iwconfig
ifconfig wlan0

# Test network connectivity
ping -c 4 google.com

# Monitor Python script manually
cd /home/pi/nyc-subway
source venv/bin/activate
python display_train.py
```

## Backup Plans

1. **If WiFi doesn't connect**: Use phone hotspot method
2. **If I2C doesn't work**: Check wiring, run i2cdetect, verify I2C enabled
3. **If display shows garbage**: Check I2C address, try different library
4. **If MTA feed fails**: Add error handling to retry, display "UPDATING..." message

## Next Steps

1. Answer questions above
2. Write modified Python script with LCD support
3. Test locally with mock display output
4. Create Raspberry Pi setup guide
5. Deploy and test

