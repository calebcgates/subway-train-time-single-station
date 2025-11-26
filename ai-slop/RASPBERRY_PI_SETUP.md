# Raspberry Pi Zero W Setup Guide
## G Train Display Installation

This guide will walk you through setting up your Raspberry Pi Zero W to display G train arrivals on a 16x2 LCD.

---

## 📋 What You'll Need

### Hardware
- ✅ Raspberry Pi Zero W (with WiFi)
- ✅ 16x2 I2C LCD with PCF8574T chip
- ✅ MicroSD card (8GB or larger)
- ✅ 5V 2.5A micro USB power supply
- ✅ 4 female-to-female jumper wires
- 🔧 Computer with SD card reader
- 🔧 Micro USB cable (for initial setup, optional)

### Software Downloads
- Raspberry Pi Imager: https://www.raspberrypi.com/software/

---

## Part 1: Prepare the SD Card

### Step 1: Flash Raspberry Pi OS

1. **Download and install Raspberry Pi Imager**
   - Mac: Download from https://www.raspberrypi.com/software/
   - Install and open the application

2. **Flash the OS**
   - Insert your microSD card into your computer
   - Open Raspberry Pi Imager
   - Click **"Choose Device"** → Select **"Raspberry Pi Zero W"**
   - Click **"Choose OS"** → Select **"Raspberry Pi OS Lite (64-bit)"**
     - *(Lite version has no desktop, perfect for this project)*
   - Click **"Choose Storage"** → Select your SD card
   - Click **"Next"**

3. **Configure Settings (IMPORTANT!)**
   - When prompted "Would you like to apply OS customization settings?" → Click **"Edit Settings"**
   
   **General Tab:**
   - ✅ Set hostname: `gtrain-display` (or whatever you prefer)
   - ✅ Set username and password:
     - Username: `pi` (or your choice)
     - Password: (choose a secure password)
   - ✅ Configure wireless LAN:
     - **SSID**: Your WiFi network name at your OTHER house
     - **Password**: Your WiFi password
     - **Wireless LAN country**: US (or your country)
   - ✅ Set locale settings:
     - Time zone: `America/New_York`
     - Keyboard layout: `us`

   **Services Tab:**
   - ✅ Enable SSH
   - Choose: **"Use password authentication"** (we'll add SSH key later)

   **Click "Save"** then **"Yes"** to apply settings
   - Click **"Yes"** to confirm erasing the SD card
   - Wait for writing and verification to complete (~5-10 minutes)

4. **Eject the SD card** when done

---

## Part 2: Add Multiple WiFi Networks (Important!)

If you want the Pi to work at BOTH your current location AND your other house, you need to add both WiFi networks.

### Option A: Before First Boot (Recommended)

1. **Re-insert the SD card** into your computer
2. **Open the SD card** (should mount as "bootfs" or similar)
3. **Find or create the file**: `wpa_supplicant.conf` in the root of the boot partition
4. **Edit the file** with both WiFi networks:

```bash
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

# Your current WiFi (for setup and testing)
network={
    ssid="YourCurrentWiFiName"
    psk="YourCurrentWiFiPassword"
    priority=10
}

# Your other house WiFi (where display will live)
network={
    ssid="YourOtherHouseWiFiName"
    psk="YourOtherHouseWiFiPassword"
    priority=5
}
```

5. **Save and eject the SD card**

### Option B: After First Boot (If you forgot)

We'll do this via SSH in Part 3.

---

## Part 3: First Boot and SSH Connection

### Step 1: Boot the Pi

1. **Insert the SD card** into your Raspberry Pi Zero W
2. **Connect power** (micro USB)
3. **Wait 60-90 seconds** for first boot (longer than normal boots)
4. The Pi should connect to your WiFi automatically

### Step 2: Find the Pi's IP Address

**Option A: Check your router's admin page**
- Look for a device named `gtrain-display` or `raspberrypi`

**Option B: Use network scanner**
```bash
# On Mac, install nmap
brew install nmap

# Scan your network (replace with your network range)
nmap -sn 192.168.1.0/24 | grep -B 2 "Raspberry Pi"
```

**Option C: Use hostname** (if mDNS works on your network)
```bash
ping gtrain-display.local
```

### Step 3: SSH into the Pi

```bash
# Replace with your Pi's IP address or hostname
ssh pi@192.168.1.XXX
# or
ssh pi@gtrain-display.local

# Enter the password you set during imaging
```

**First login message**: Type `yes` to accept the fingerprint

🎉 **You're now connected to your Raspberry Pi!**

---

## Part 4: Initial Configuration

### Step 1: Update the System

```bash
# Update package lists and upgrade
sudo apt-get update
sudo apt-get upgrade -y

# This may take 10-15 minutes on Pi Zero W
```

### Step 2: Install Required System Packages

```bash
# Install I2C tools and Python development packages
sudo apt-get install -y i2c-tools python3-pip python3-venv python3-dev git

# Install system libraries needed for RPLCD
sudo apt-get install -y python3-smbus
```

### Step 3: Enable I2C Interface

```bash
# Open configuration tool
sudo raspi-config
```

**Navigate:**
1. Select **"3 Interface Options"**
2. Select **"I5 I2C"**
3. Select **"Yes"** to enable
4. Select **"Ok"**
5. Select **"Finish"**
6. Select **"Yes"** to reboot

**Wait for Pi to reboot** (~30 seconds), then SSH back in.

---

## Part 5: Wire the LCD Display

### Step 1: Identify the Pins

**Raspberry Pi Zero W Pinout:**
```
    3.3V  [1] [2]  5V     ← LCD VCC connects here
     SDA  [3] [4]  5V
     SCL  [5] [6]  GND    ← LCD GND connects here
    GPIO7 [7] [8]  GPIO14
      GND [9] [10] GPIO15
```

**LCD I2C Module Pins:**
- VCC (or VDD) - Power (5V)
- GND - Ground
- SDA - Data line
- SCL - Clock line

### Step 2: Connect the Wires

**With Pi POWERED OFF:**

| LCD Pin | →  | Pi Zero W Pin | Wire Color (suggestion) |
|---------|-----|---------------|------------------------|
| VCC     | →  | Pin 2 (5V)    | Red                    |
| GND     | →  | Pin 6 (GND)   | Black                  |
| SDA     | →  | Pin 3 (SDA)   | Blue or Green          |
| SCL     | →  | Pin 5 (SCL)   | Yellow or White        |

**Power on the Pi**

### Step 3: Test I2C Connection

```bash
# Detect I2C devices
sudo i2cdetect -y 1
```

**Expected output:**
```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- 27 -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
...
```

The number `27` (or `3f`) is your LCD's I2C address. **Remember this!**

**If you see nothing:**
- Check your wiring
- Make sure I2C is enabled in raspi-config
- Try powering off and on again

---

## Part 6: Install the Project

### Step 1: Create Project Directory

```bash
# Navigate to home directory
cd ~

# Create project directory
mkdir nyc-subway
cd nyc-subway
```

### Step 2: Transfer Project Files from Your Mac

**On your Mac** (in a new terminal window):

```bash
# Navigate to your project directory
cd /Users/calebgates/PycharmProjects/nyc-subway

# Transfer files to Pi (replace IP address)
scp display_train.py requirements.txt pi@192.168.1.XXX:~/nyc-subway/

# Or if hostname works:
scp display_train.py requirements.txt pi@gtrain-display.local:~/nyc-subway/
```

**Alternative: Manual Copy**
```bash
# On Pi, create the files manually
nano ~/nyc-subway/display_train.py
# Copy and paste the content, Ctrl+X to save

nano ~/nyc-subway/requirements.txt
# Copy and paste the content, Ctrl+X to save
```

### Step 3: Set Up Python Virtual Environment

**Back on the Pi:**

```bash
cd ~/nyc-subway

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Install LCD library
pip install RPLCD

# This may take 5-10 minutes on Pi Zero W
```

### Step 4: Update LCD I2C Address (if needed)

If your LCD uses address `0x3f` instead of `0x27`:

```bash
nano display_train.py

# Find this line (around line 22):
LCD_ADDRESS = 0x27

# Change to:
LCD_ADDRESS = 0x3f

# Save: Ctrl+X, Y, Enter
```

---

## Part 7: Test the Display

### Step 1: Manual Test

```bash
cd ~/nyc-subway
source venv/bin/activate
python display_train.py
```

**Expected behavior:**
1. LCD shows "Fetching train data..."
2. After a moment, shows northbound trains (QUEENS)
3. After 4 seconds, switches to southbound trains (BROOKLYN)
4. Alternates every 4 seconds
5. Terminal shows updates every 30 seconds

**Test for a few minutes** to make sure it's working properly.

**Stop the script:** Press `Ctrl+C`

---

## Part 8: Configure Auto-Start on Boot

### Step 1: Create systemd Service

```bash
# Create service file
sudo nano /etc/systemd/system/gtrain-display.service
```

**Paste this content** (adjust username if not 'pi'):

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
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

**Save and exit:** `Ctrl+X`, `Y`, `Enter`

### Step 2: Enable and Start Service

```bash
# Reload systemd to recognize new service
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable gtrain-display.service

# Start service now
sudo systemctl start gtrain-display.service

# Check status
sudo systemctl status gtrain-display.service
```

**Expected output:**
```
● gtrain-display.service - G Train Display Service
   Loaded: loaded (/etc/systemd/system/gtrain-display.service; enabled)
   Active: active (running) since ...
```

Press `q` to exit status view.

### Step 3: Test Auto-Start

```bash
# Reboot the Pi
sudo reboot
```

**Wait 60-90 seconds**, the display should start automatically showing trains!

---

## Part 9: Set Up SSH Key for Easy Access

This allows you to SSH without a password and is more secure.

### Step 1: Generate SSH Key on Your Mac (if you don't have one)

**On your Mac:**

```bash
# Check if you already have an SSH key
ls ~/.ssh/id_rsa.pub

# If not found, generate one
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
# Press Enter to accept default location
# Enter passphrase (optional but recommended)
```

### Step 2: Copy SSH Key to Pi

**On your Mac:**

```bash
# Copy your public key to the Pi
ssh-copy-id pi@192.168.1.XXX
# or
ssh-copy-id pi@gtrain-display.local

# Enter your Pi password when prompted
```

### Step 3: Test Key-Based Login

```bash
# Try to SSH without password
ssh pi@192.168.1.XXX

# Should connect without asking for password!
```

---

## Part 10: Useful Maintenance Commands

### Check Service Status

```bash
# View service status
sudo systemctl status gtrain-display.service

# View live logs
sudo journalctl -u gtrain-display.service -f

# View last 50 log lines
sudo journalctl -u gtrain-display.service -n 50

# Stop service
sudo systemctl stop gtrain-display.service

# Start service
sudo systemctl start gtrain-display.service

# Restart service
sudo systemctl restart gtrain-display.service
```

### Update the Script

```bash
# Stop the service
sudo systemctl stop gtrain-display.service

# Edit the script
nano ~/nyc-subway/display_train.py

# Save changes (Ctrl+X, Y, Enter)

# Start service again
sudo systemctl start gtrain-display.service
```

### Check WiFi Status

```bash
# Check WiFi connection
iwconfig

# Check IP address
hostname -I

# Test internet connectivity
ping -c 4 google.com
```

### System Information

```bash
# Check CPU temperature
vcgencmd measure_temp

# Check memory usage
free -h

# Check disk space
df -h
```

---

## Part 11: Taking It to Your Other House

### What Should Happen:

1. **Unplug the Pi** at current location
2. **Transport it** to your other house
3. **Plug it in** at the other house
4. **Wait 60-90 seconds** for boot
5. **Pi automatically connects** to the WiFi you configured
6. **Display starts** automatically showing trains!

### If It Doesn't Connect to WiFi:

**Option A: Use Phone Hotspot**
1. Set up a mobile hotspot with the SSID/password you configured
2. Connect your laptop to the hotspot
3. SSH into the Pi: `ssh pi@gtrain-display.local`
4. Add the new WiFi network:
```bash
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
# Add new network block, save
sudo reboot
```

**Option B: Bring SD Card Reader**
1. Power off Pi
2. Remove SD card
3. Insert into laptop
4. Edit `wpa_supplicant.conf` on boot partition
5. Add new WiFi credentials
6. Eject, reinsert into Pi, boot

---

## Troubleshooting

### LCD Shows Garbage Characters

**Problem:** Wrong I2C address or connection issue

**Solution:**
```bash
# Check I2C address
sudo i2cdetect -y 1

# Update script with correct address
nano ~/nyc-subway/display_train.py
# Change LCD_ADDRESS = 0x27 to correct address

# Restart service
sudo systemctl restart gtrain-display.service
```

### LCD is Blank

**Problem:** No power or wrong contrast setting

**Solution:**
1. Check wiring (especially VCC and GND)
2. Adjust potentiometer on LCD backpack with small screwdriver
3. Check I2C connection: `sudo i2cdetect -y 1`

### Display Shows "Network Error"

**Problem:** No internet connection

**Solution:**
```bash
# Check WiFi status
iwconfig

# Check if connected to network
ping -c 4 google.com

# Restart WiFi
sudo systemctl restart dhcpcd

# Check service logs
sudo journalctl -u gtrain-display.service -n 50
```

### Service Won't Start

**Problem:** Python error or missing dependencies

**Solution:**
```bash
# Check service status for errors
sudo systemctl status gtrain-display.service

# View detailed logs
sudo journalctl -u gtrain-display.service -n 100

# Test script manually
cd ~/nyc-subway
source venv/bin/activate
python display_train.py

# Look for error messages
```

### Trains Show "NA" All the Time

**Problem:** MTA feed issue or incorrect stop ID

**Solution:**
1. Test on your Mac first: `python read_g_train.py`
2. Check if MTA feed is working: https://api-endpoint.mta.info/
3. Verify you're checking stop G22 (Greenpoint Avenue)

---

## 🎉 You're Done!

Your G Train display should now be running automatically and showing real-time arrivals!

### Quick Reference Card

```bash
# SSH into Pi
ssh pi@gtrain-display.local

# View live display logs
sudo journalctl -u gtrain-display.service -f

# Restart display service
sudo systemctl restart gtrain-display.service

# Stop display service
sudo systemctl stop gtrain-display.service

# Start display service
sudo systemctl start gtrain-display.service

# Edit display script
nano ~/nyc-subway/display_train.py

# Reboot Pi
sudo reboot

# Shutdown Pi
sudo shutdown -h now
```

---

**Questions or issues?** Check the troubleshooting section or review the service logs!

