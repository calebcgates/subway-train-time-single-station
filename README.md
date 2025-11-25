# NYC Subway G Train Tracker

This script tracks real-time arrivals for the G train at Greenpoint Avenue station.

## Setup

### Install Dependencies

```bash
# Activate the virtual environment
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

## Usage

```bash
# Make sure you're in the project directory
cd /Users/calebgates/PycharmProjects/nyc-subway

# Activate virtual environment
source venv/bin/activate

# Run the script
python read_g_train.py
```

The script will show:
- **Northbound trains** (to Queens)
- **Southbound trains** (to Brooklyn)
- Arrival times and minutes away

## About

- **Station**: Greenpoint Avenue
- **Stop IDs**: G22N (Northbound), G22S (Southbound)
- **Line**: G Train
- **Data Source**: [MTA Real-time Data Feeds](https://api-endpoint.mta.info/) (free, no API key required)

## Example Output

```
Trains arriving at Greenpoint Avenue (G22):

Northbound (to Queens)
  Arrives: 20:35:23 (4 minutes)

Southbound (to Brooklyn)
  Arrives: 20:31:00 (0 minutes)
```
