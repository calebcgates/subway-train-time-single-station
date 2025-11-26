# NYC Subway Train Display

A Raspberry Pi project that displays real-time NYC subway arrival times on a 16x2 LCD screen.

## Project Origin

I created this project so that my girlfriend could see when the train near her apartment would arrive. It's a 6-minute walk to the station, and the train only comes every 12 minutes with inconsistent spacing.

I found that the MTA has a public set of APIs that don't require authentication. It's not a JSON API, so you do need a Python library to decode the responses.

My goal was to run this on a Raspberry Pi because I have a bunch of them. I knew I could set it up at my home and then pre-configure the WiFi so that it would connect automatically when I plugged it in at the house I was bringing it to.

## Hardware Setup

### Components Needed
- Raspberry Pi (any model with I2C support)
- 16x2 I2C LCD display
- Micro SD card (8GB or larger)
- Power supply
- Jumper wires

### Wiring
Connect the I2C LCD display to your Raspberry Pi:
- VCC → 5V
- GND → Ground  
- SDA → GPIO 2 (SDA)
- SCL → GPIO 3 (SCL)

**LCD Contrast Tip:** There's a small potentiometer on the back of the LCD that you can twist to adjust the contrast. I used an exacto knife to find the perfect setting.

## Software Installation

### Initial Raspberry Pi Setup

I did the initial setup on an old Pi and was then forced to upgrade from the 2017 OS to the 2025 OS because pip wouldn't install any of my dependencies.

Hours later—literally the worst part of projects like this—I had an SD card formatted to ExFAT and then copied the 1.1GB ISO onto it.

**Note:** I tried to use the Raspberry Pi Imager, but it kept rejecting my SD card midway. It was either the installer or my SD-to-microSD adapter. I got a new adapter and just downloaded the entire image first from their website. That made it much faster to copy onto the SD card from the command line—though it did take a while to finalize.

I then had to boot the Pi and go through the startup (thank god I have a micro HDMI to HDMI converter, a dongle for micro USB to USB 2.0 with a keyboard and mouse, and an extra monitor on my desk).

I did the manual setup and chose the localization, then turned on SSH mode.

### Installing the Project

Once I had the OS and SSH turned on, I connected via SSH from my Mac and pushed the files I had worked on locally to the Pi, moved them to the right folder, created a venv, activated it, installed requirements, and ran the script.

```bash
# Clone or copy this repository to your Raspberry Pi
cd ~
mkdir nyc-subway
cd nyc-subway

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the display
python3 display_train.py
```

### Enable I2C on Raspberry Pi

```bash
sudo raspi-config
# Navigate to: Interface Options → I2C → Enable

# Verify I2C device is detected
sudo i2cdetect -y 1
```

### WiFi Configuration

I also had to add the WiFi for the other house. Edit `/etc/wpa_supplicant/wpa_supplicant.conf` to add your network:

```
network={
    ssid="Your_Network_Name"
    psk="Your_Password"
}
```

### Run on Startup

To set the code to run on startup, create a systemd service:

```bash
sudo nano /etc/systemd/system/gtrain.service
```

Add the following content:

```ini
[Unit]
Description=G Train Display
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/nyc-subway
ExecStart=/home/pi/nyc-subway/venv/bin/python3 /home/pi/nyc-subway/display_train.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable gtrain.service
sudo systemctl start gtrain.service

# Check status
sudo systemctl status gtrain.service
```

## Configuration

The `.py` file was designed to pull from the subway API, format the data, and then display it on the attached 16-char by 2-char screen.

### Customizing for Your Station

If you choose to clone this repo for yourself, you'll have to edit the following in `display_train.py`:

1. **Subway stop address** (lines 88, 98):
   - Find your stop ID from the [MTA GTFS feeds](https://api.mta.info/)
   - Replace `'G22N'` and `'G22S'` with your station codes

2. **Direction labels** (line 129):
   - Replace `"QUEENS"` and `"BROOKLYN"` with your line's directions

3. **MTA Feed URL** (line 24):
   - Replace with your subway line's feed URL
   - Available feeds: https://api.mta.info/

4. **Potentially some of the API parsing logic** depending on your train line names

## Key Files

- **`display_train.py`** - Main program that fetches train data and controls the LCD display
- **`requirements.txt`** - Python dependencies needed for the project

## How It Works

The display alternates every 4 seconds between showing:
1. Next 2 northbound trains
2. Next 2 southbound trains

The program refreshes train data from the MTA API every 30 seconds.

## Troubleshooting

### LCD Not Working
- Check I2C is enabled: `sudo raspi-config`
- Verify wiring and I2C address: `sudo i2cdetect -y 1`
- Try alternate I2C address `0x3f` if `0x27` doesn't work (line 27 in display_train.py)
- Adjust contrast using the potentiometer on the back of the LCD

### No Train Data
- Check WiFi connection: `ping 8.8.8.8`
- Verify MTA API is accessible: `curl https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g`
- Check system logs: `journalctl -u gtrain.service -f`

### Testing Without LCD
The code can run in test mode on any computer. If the LCD library isn't available (like on macOS), it will print a simulated display to the console instead.

```bash
# On Mac or any system without the LCD
python3 display_train.py
```

## Challenges I Faced

Some challenges I faced were:
- The contrast of the screen (solved with the potentiometer adjustment)
- Installing the OS on the SD card (installer issues)
- Upgrading from an old Raspberry Pi OS
- WiFi configuration for remote deployment
- Setting up the service to run on boot

## Good Luck!

If you build this project, I hope this guide helps you avoid some of the pitfalls I encountered. Feel free to adapt it for any NYC subway line!

---

*Made with ❤️ for better train timing awareness*


Pushing Updates:
Mac: scp /Users/calebgates/PycharmProjects/nyc-subway/display_train.py pi@raspberrypi.local:~/nyc-subway/
Pi:  sudo systemctl restart gtrain-display.service
