# NYC Subway G Train Tracker

Real-time G train arrivals for Greenpoint Avenue station - available as both a command-line tool and a Raspberry Pi LCD display.

## 🚇 Features

- **Real-time MTA data** - Live train arrivals from official MTA GTFS feed
- **CLI tool** - Simple command-line display of all upcoming trains
- **LCD display** - Raspberry Pi Zero W with 16x2 LCD for persistent display
- **Auto-updating** - Refreshes every 30 seconds
- **Dual direction** - Shows both northbound (Queens) and southbound (Brooklyn) trains

## 📋 What's Included

### For Testing/Development (Mac/PC)
- `read_g_train.py` - Command-line tool showing all upcoming trains

### For Raspberry Pi LCD Display
- `display_train.py` - LCD display script with auto-alternating screens
- `RASPBERRY_PI_SETUP.md` - Complete setup guide for Pi Zero W
- `QUICK_START.md` - Quick reference for maintenance
- `scratchpad.md` - Project planning and requirements

## 🚀 Quick Start

### Option 1: Command-Line Tool (Mac/PC)

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the script
python read_g_train.py
```

**Output:**
```
Trains arriving at Greenpoint Avenue (G22):

Northbound (to Queens)
  Arrives: 20:35:23 (4 minutes)

Southbound (to Brooklyn)
  Arrives: 20:31:00 (0 minutes)

Northbound (to Queens)
  Arrives: 20:51:23 (20 minutes)
```

### Option 2: Raspberry Pi LCD Display

**See full guide:** [`RASPBERRY_PI_SETUP.md`](RASPBERRY_PI_SETUP.md)

**Display format (alternates every 4 seconds):**

Northbound screen:
```
QUEENS       4 M
QUEENS      11 M
```

Southbound screen:
```
BROOKLYN     1 M
BROOKLYN    13 M
```

**Hardware needed:**
- Raspberry Pi Zero W
- 16x2 I2C LCD (PCF8574)
- 4 jumper wires
- 5V power supply

## 📖 Documentation

- **[RASPBERRY_PI_SETUP.md](RASPBERRY_PI_SETUP.md)** - Complete setup guide from SD card to running display
- **[QUICK_START.md](QUICK_START.md)** - Quick reference for common tasks
- **[scratchpad.md](scratchpad.md)** - Project requirements and planning

## 🔧 Configuration

### Display Settings (display_train.py)

```python
REFRESH_INTERVAL = 30  # Seconds between MTA data fetches
DISPLAY_INTERVAL = 4   # Seconds to show each direction
LCD_ADDRESS = 0x27     # I2C address (try 0x3f if issues)
```

## 📡 About the Data

- **Station**: Greenpoint Avenue (G22)
- **Stop IDs**: 
  - G22N - Northbound (to Queens)
  - G22S - Southbound (to Brooklyn)
- **Line**: G Train
- **Data Source**: [MTA Real-time Data Feeds](https://api-endpoint.mta.info/)
- **API Key**: Not required (free public access)
- **Update Frequency**: MTA updates every ~30 seconds

## 🐛 Troubleshooting

### Command-line tool issues
```bash
# Make sure dependencies are installed
pip install -r requirements.txt

# Check internet connection
ping api-endpoint.mta.info
```

### Raspberry Pi issues

See [QUICK_START.md](QUICK_START.md) troubleshooting section or [RASPBERRY_PI_SETUP.md](RASPBERRY_PI_SETUP.md) for detailed help.

Common fixes:
```bash
# Check LCD connection
sudo i2cdetect -y 1

# View service logs
sudo journalctl -u gtrain-display.service -f

# Restart display
sudo systemctl restart gtrain-display.service
```

## 📦 Requirements

### Python Dependencies
- `gtfs-realtime-bindings` - Parse MTA GTFS data
- `protobuf` - Protocol buffer support
- `RPLCD` - Raspberry Pi LCD library (Pi only)

### System Requirements
- Python 3.7+
- Internet connection
- For Pi: I2C enabled, GPIO access

## 🎯 Project Structure

```
nyc-subway/
├── read_g_train.py          # CLI tool (all trains)
├── display_train.py         # LCD display script (top 2+2)
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── RASPBERRY_PI_SETUP.md   # Complete Pi setup guide
├── QUICK_START.md          # Quick reference
└── scratchpad.md           # Planning notes
```

## 🙏 Credits

- MTA for providing free real-time transit data
- GTFS Realtime for the data format specification
