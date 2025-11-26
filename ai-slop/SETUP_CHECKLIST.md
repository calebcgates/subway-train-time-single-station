# Setup Checklist - G Train Display

Print this and check off items as you complete them!

---

## 📦 Pre-Setup (Before You Start)

- [X] Raspberry Pi Zero W (with WiFi)
- [X] 16x2 I2C LCD with PCF8574T chip
- [X] MicroSD card (8GB+)
- [X] SD card reader for computer
- [X] 5V 2.5A micro USB power supply
- [X] 4 female-to-female jumper wires
- [X] Computer with Raspberry Pi Imager installed
- [ ] WiFi credentials for BOTH locations written down

**WiFi Info:**
- Current location SSID: _________________ Password: _________________
- Other house SSID: _________________ Password: _________________

---

## 🔧 Part 1: SD Card Preparation (30 minutes)

- [X] Download and install Raspberry Pi Imager
- [X] Insert SD card into computer
- [X] Open Raspberry Pi Imager
- [X] Select Device: Raspberry Pi Zero W
- [X] Select OS: Raspberry Pi OS Lite (64-bit)
- [X] Select Storage: Your SD card
- [X] Click "Next" → "Edit Settings"


DONE 

### Settings to Configure:
- [ ] Hostname: `gtrain-display`
- [ ] Username: `pi` (or your choice)
- [ ] Password: _________________ (write it down!)
- [ ] Configure WiFi: Enter BOTH locations (see RASPBERRY_PI_SETUP.md)
- [ ] WiFi Country: US
- [ ] Timezone: America/New_York
- [ ] Keyboard: us
- [ ] Enable SSH: Yes (password authentication)

- [ ] Click "Save" → "Yes" → "Yes" to write
- [ ] Wait for writing and verification (~10 minutes)
- [ ] Eject SD card safely

---

## 🚀 Part 2: First Boot (15 minutes)

DONE

- [ ] Insert SD card into Raspberry Pi Zero W
- [ ] Connect power via micro USB
- [ ] Wait 60-90 seconds for first boot
- [ ] Find Pi's IP address (check router or use network scanner)
- [ ] Write down IP: _________________
- [ ] SSH into Pi: `ssh pi@192.168.1.XXX` or `ssh pi@gtrain-display.local`
- [ ] Accept fingerprint (type `yes`)
- [ ] Enter password
- [ ] 🎉 You're connected!

---

## 🔄 Part 3: System Update (15-20 minutes)

Run these commands on the Pi:

- [ ] `sudo apt-get update`
- [ ] `sudo apt-get upgrade -y` (takes 10-15 minutes)
- [ ] `sudo apt-get install -y i2c-tools python3-pip python3-venv python3-dev git python3-smbus`

---

## ⚙️ Part 4: Enable I2C (5 minutes)

- [ ] Run: `sudo raspi-config`
- [ ] Navigate to: Interface Options → I2C
- [ ] Select "Yes" to enable
- [ ] Select "Ok" → "Finish"
- [ ] Select "Yes" to reboot
- [ ] Wait 30 seconds, then SSH back in

---

## 🔌 Part 5: Wire LCD (10 minutes)

**POWER OFF THE PI FIRST:** `sudo shutdown -h now`, wait 30 seconds, unplug

### Wiring Checklist:

- [ ] LCD VCC → Pi Pin 2 (5V) - Red wire recommended
- [ ] LCD GND → Pi Pin 6 (GND) - Black wire recommended  
- [ ] LCD SDA → Pi Pin 3 (GPIO 2 / SDA) - Blue/Green wire
- [ ] LCD SCL → Pi Pin 5 (GPIO 3 / SCL) - Yellow/White wire
- [ ] Double-check all connections
- [ ] Power on the Pi

### Test I2C Connection:

- [ ] SSH back into Pi
- [ ] Run: `sudo i2cdetect -y 1`
- [ ] Note the address shown:  27  (usually `27` or `3f`)
- [ ] If nothing shows, re-check wiring!

---

## 📥 Part 6: Install Project (15 minutes)

### On Your Mac:

- [ ] Open terminal
- [ ] Navigate to: `cd /Users/calebgates/PycharmProjects/nyc-subway`
- [ ] Transfer files: 
  ```bash
  scp display_train.py requirements.txt pi@192.168.1.XXX:~/
  ```
  (Replace XXX with Pi's IP or use `gtrain-display.local`)

### Back on the Pi:

- [ ] `mkdir nyc-subway`
- [ ] `mv display_train.py requirements.txt nyc-subway/`
- [ ] `cd nyc-subway`
- [ ] `python3 -m venv venv`
- [ ] `source venv/bin/activate`
- [ ] `pip install --upgrade pip`
- [ ] `pip install -r requirements.txt` (takes 5-10 minutes)
- [ ] `pip install RPLCD`

---

## 🧪 Part 7: Test Display (10 minutes)

- [ ] Make sure you're in: `cd ~/nyc-subway`
- [ ] Activate venv: `source venv/bin/activate`
- [ ] If LCD address is NOT 0x27, edit: `nano display_train.py`
  - [ ] Change line 21: `LCD_ADDRESS = 0x3f` (or your address)
  - [ ] Save: Ctrl+X, Y, Enter
- [ ] Run script: `python display_train.py`

### Verify:

- [ ] LCD backlight turns on
- [ ] "Fetching train data..." appears
- [ ] After ~5 seconds, trains appear
- [ ] Screen shows "QUEENS" with 2 trains
- [ ] After 4 seconds, switches to "BROOKLYN" 
- [ ] Alternates every 4 seconds
- [ ] Terminal shows update messages every 30 seconds

**If working correctly:** Press Ctrl+C to stop

**If issues:** See troubleshooting in RASPBERRY_PI_SETUP.md

---

## 🤖 Part 8: Configure Auto-Start (10 minutes)

- [ ] Create service: `sudo nano /etc/systemd/system/gtrain-display.service`
- [ ] Copy the service file content from RASPBERRY_PI_SETUP.md Part 8
- [ ] Save: Ctrl+X, Y, Enter
- [ ] `sudo systemctl daemon-reload`
- [ ] `sudo systemctl enable gtrain-display.service`
- [ ] `sudo systemctl start gtrain-display.service`
- [ ] `sudo systemctl status gtrain-display.service`
- [ ] Verify it says "active (running)" in green
- [ ] Press `q` to exit

---

## 🔐 Part 9: SSH Key Setup (5 minutes)

### On Your Mac:

- [ ] Check for existing key: `ls ~/.ssh/id_rsa.pub`
- [ ] If not found, create: `ssh-keygen -t rsa -b 4096`
- [ ] Copy to Pi: `ssh-copy-id pi@192.168.1.XXX`
- [ ] Test: `ssh pi@192.168.1.XXX` (should connect without password)

---

## ✅ Part 10: Final Test (5 minutes)

- [ ] While SSH'd into Pi: `sudo reboot`
- [ ] Wait 60-90 seconds
- [ ] Display should start automatically showing trains
- [ ] SSH back in to verify: `sudo systemctl status gtrain-display.service`
- [ ] Should show "active (running)"

---

## 🏠 Part 11: Deployment Checklist

When taking to your other house:

- [ ] Unplug Pi from power
- [ ] Keep LCD wired (don't disconnect)
- [ ] Transport carefully
- [ ] At other house: Plug in power
- [ ] Wait 60-90 seconds for boot
- [ ] Display should start automatically!

### If WiFi Doesn't Connect:

- [ ] Try: `ssh pi@gtrain-display.local` from laptop
- [ ] Check WiFi: `iwconfig`
- [ ] Add network: See RASPBERRY_PI_SETUP.md Part 11

---

## 📋 Post-Installation

- [ ] Let it run for 24 hours to verify stability
- [ ] Check logs: `sudo journalctl -u gtrain-display.service -n 50`
- [ ] Note any issues: _________________________________
- [ ] Add IP to your password manager: _________________
- [ ] Bookmark this checklist for future reference

---

## 🆘 Quick Troubleshooting

**LCD shows garbage:**
- [ ] Run: `sudo i2cdetect -y 1`
- [ ] Update LCD_ADDRESS in script if different
- [ ] Adjust contrast pot on LCD backpack

**Service not running:**
- [ ] `sudo systemctl status gtrain-display.service`
- [ ] `sudo journalctl -u gtrain-display.service -n 50`
- [ ] Test manually: `cd ~/nyc-subway && source venv/bin/activate && python display_train.py`

**Network error:**
- [ ] Check WiFi: `iwconfig`
- [ ] Test connection: `ping -c 4 google.com`
- [ ] Check MTA: `ping -c 4 api-endpoint.mta.info`

---

## 🎉 Success!

Once everything is checked off, you have a fully functional G train display!

**Useful commands to remember:**
```bash
# View logs
sudo journalctl -u gtrain-display.service -f

# Restart display
sudo systemctl restart gtrain-display.service

# Reboot Pi
sudo reboot

# Shutdown Pi
sudo shutdown -h now
```

**Keep this checklist** for when you need to troubleshoot or set up another one!

---

**Setup Date:** _______________  
**Pi IP Address:** _______________  
**LCD I2C Address:** _______________  
**Notes:** _______________________________________________

