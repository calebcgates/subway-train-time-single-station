#!/usr/bin/env python3
"""
G Train Display for 16x2 I2C LCD
Shows next 3 northbound and 3 southbound trains at Greenpoint Avenue

Two display modes:
- STATIC: All 3 trains per direction on 2 lines (default)
- DYNAMIC: Cycles through 4 pages showing trains individually
"""

from google.transit import gtfs_realtime_pb2
import urllib.request
from datetime import datetime
import time
import sys

# Try to import LCD library (will fail on Mac, that's OK for testing)
try:
    from RPLCD.i2c import CharLCD
    LCD_AVAILABLE = True
except ImportError:
    LCD_AVAILABLE = False
    print("LCD library not available - running in test mode")
    print("Install on Raspberry Pi with: pip install RPLCD")

# Configuration
MTA_FEED_URL = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g'
REFRESH_INTERVAL = 30  # Seconds between data fetches
DISPLAY_INTERVAL = 1.5   # Seconds to show each page (DYNAMIC mode only)
LCD_ADDRESS = 0x27     # Default I2C address, change to 0x3f if needed

# Display Mode: 'STATIC' or 'DYNAMIC'
# STATIC: Shows all 3 trains for both directions on 2 lines (updates every 30s)
# DYNAMIC: Cycles through 4 pages showing trains individually (updates every 1.5s)
DISPLAY_MODE = 'STATIC'  # Change to 'DYNAMIC' for cycling display

class TrainDisplay:
    def __init__(self):
        """Initialize the LCD display"""
        self.lcd = None
        if LCD_AVAILABLE:
            try:
                # Initialize LCD: 16 chars wide, 2 lines, I2C address
                self.lcd = CharLCD(i2c_expander='PCF8574', address=LCD_ADDRESS,
                                  port=1, cols=16, rows=2, dotsize=8)
                self.lcd.clear()
                self.write_lines("G Train Display", "Starting...")
                print("LCD initialized successfully")
            except Exception as e:
                print(f"Error initializing LCD: {e}")
                print("Make sure I2C is enabled: sudo raspi-config")
                print("Check wiring and I2C address: sudo i2cdetect -y 1")
                sys.exit(1)
    
    def write_lines(self, line1, line2):
        """Write two lines to the LCD"""
        if self.lcd:
            self.lcd.clear()
            self.lcd.write_string(line1)
            self.lcd.crlf()
            self.lcd.write_string(line2)
        else:
            # Test mode - print to console
            print(f"┌{'─' * 16}┐")
            print(f"│{line1:16}│")
            print(f"│{line2:16}│")
            print(f"└{'─' * 16}┘")
    
    def cleanup(self):
        """Clear display and cleanup"""
        if self.lcd:
            self.lcd.clear()
            self.lcd.close()

class TrainTracker:
    def __init__(self):
        self.northbound_trains = []
        self.southbound_trains = []
        self.last_update = None
    
    def fetch_trains(self):
        """Fetch train data from MTA feed"""
        try:
            feed = gtfs_realtime_pb2.FeedMessage()
            response = urllib.request.urlopen(MTA_FEED_URL, timeout=10)
            feed.ParseFromString(response.read())
            
            northbound = []
            southbound = []
            now = datetime.now()
            
            # Parse feed for Greenpoint Avenue (G22)
            for entity in feed.entity:
                if entity.HasField('trip_update'):
                    for stop in entity.trip_update.stop_time_update:
                        if stop.stop_id == 'G22N' and stop.HasField('arrival'):
                            arrival_time = datetime.fromtimestamp(stop.arrival.time)
                            minutes = int((arrival_time - now).total_seconds() / 60)
                            if minutes >= 0:  # Only future arrivals
                                northbound.append({
                                    'arrival_time': arrival_time,
                                    'minutes': minutes
                                })
                            break  # Only check first stop match per train
                        
                        elif stop.stop_id == 'G22S' and stop.HasField('arrival'):
                            arrival_time = datetime.fromtimestamp(stop.arrival.time)
                            minutes = int((arrival_time - now).total_seconds() / 60)
                            if minutes >= 0:  # Only future arrivals
                                southbound.append({
                                    'arrival_time': arrival_time,
                                    'minutes': minutes
                                })
                            break  # Only check first stop match per train
            
            # Sort by arrival time and keep top 3
            northbound.sort(key=lambda x: x['arrival_time'])
            southbound.sort(key=lambda x: x['arrival_time'])
            
            self.northbound_trains = northbound[:3]
            self.southbound_trains = southbound[:3]
            self.last_update = datetime.now()
            
            print(f"✓ Updated: {len(northbound)} northbound, {len(southbound)} southbound trains found")
            return True
            
        except urllib.error.URLError as e:
            print(f"✗ Network error: {e}")
            return False
        except Exception as e:
            print(f"✗ Error fetching trains: {e}")
            return False
    
    def format_display_lines(self, direction='north', train_indices=[0, 1]):
        """Format two lines for the 16x2 display (DYNAMIC mode)
        
        Args:
            direction: 'north' or 'south'
            train_indices: List of train indices to display (e.g., [0, 1] or [2])
        """
        trains = self.northbound_trains if direction == 'north' else self.southbound_trains
        label = "QUEENS" if direction == 'north' else "BROOKLYN"
        
        lines = []
        for idx in train_indices:
            if idx < len(trains):
                minutes = trains[idx]['minutes']
                # Format: "BROOKLYN     1 M" (16 chars total)
                # Label is left-aligned, time is right-aligned
                if minutes < 100:
                    time_str = f"{minutes:2} M"
                else:
                    time_str = "99+M"
                
                # Calculate spacing: 16 total - len(label) - len(time_str)
                spaces = 16 - len(label) - len(time_str)
                line = f"{label}{' ' * spaces}{time_str}"
            else:
                # No train available - show NA
                time_str = "NA"
                spaces = 16 - len(label) - len(time_str)
                line = f"{label}{' ' * spaces}{time_str}"
            
            lines.append(line)
        
        # If only one train index provided, add blank line
        if len(train_indices) == 1:
            lines.append(" " * 16)
        
        return lines[0], lines[1]
    
    def format_static_display(self):
        """Format both directions on 2 lines (STATIC mode)
        
        Returns two lines showing 3 trains for each direction:
        Line 1: QUEENS 03|09|15M
        Line 2: BRKLYN 05|12|18M
        
        Format: LABEL MM|MM|MMM (16 chars total)
        """
        lines = []
        
        for direction in ['north', 'south']:
            trains = self.southbound_trains if direction == 'south' else self.northbound_trains
            label = "BRKLYN" if direction == 'south' else "QUEENS"
            
            # Get times for up to 3 trains
            times = []
            for i in range(3):
                if i < len(trains):
                    minutes = trains[i]['minutes']
                    if minutes < 100:
                        times.append(f"{minutes:02d}")
                    else:
                        times.append("99")
                else:
                    times.append("--")
            
            # Format: "BRKLYN 05|12|18M" (16 chars)
            # BRKLYN=6, space=1, times=8 (00|00|00), M=1 = 16 total
            time_str = f" {times[0]} {times[1]} {times[2]}"
            line = f"{label} {time_str}"
            lines.append(line)
        
        return lines[0], lines[1]

def main():
    """Main loop"""
    print("=" * 50)
    print("NYC G Train Display - Greenpoint Avenue (G22)")
    print("=" * 50)
    print(f"Display mode: {DISPLAY_MODE}")
    print(f"Refresh interval: {REFRESH_INTERVAL} seconds")
    if DISPLAY_MODE == 'DYNAMIC':
        print(f"Display interval: {DISPLAY_INTERVAL} seconds per page")
        print("Shows 3 trains each direction (4 pages total)")
    else:
        print("Shows all 3 trains per direction on 2 lines")
    print("Press Ctrl+C to exit")
    print("=" * 50)
    
    # Initialize display and tracker
    display = TrainDisplay()
    tracker = TrainTracker()
    
    # Initial fetch
    display.write_lines("Fetching train", "data...")
    if not tracker.fetch_trains():
        display.write_lines("Network Error", "Check WiFi")
        time.sleep(5)
    
    last_fetch_time = time.time()
    
    try:
        while True:
            # Fetch new data if interval has passed
            if time.time() - last_fetch_time >= REFRESH_INTERVAL:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Refreshing data...")
                if tracker.fetch_trains():
                    last_fetch_time = time.time()
                    
                    # In STATIC mode, update display immediately after fetching
                    if DISPLAY_MODE == 'STATIC':
                        line1, line2 = tracker.format_static_display()
                        display.write_lines(line1, line2)
                else:
                    # On error, wait a bit before retrying
                    time.sleep(5)
                    continue
            
            if DISPLAY_MODE == 'DYNAMIC':
                # Show northbound trains - page 1 (trains 1 & 2)
                line1, line2 = tracker.format_display_lines('north', [0, 1])
                display.write_lines(line1, line2)
                time.sleep(DISPLAY_INTERVAL)
                
                # Show northbound trains - page 2 (train 3)
                line1, line2 = tracker.format_display_lines('north', [2])
                display.write_lines(line1, line2)
                time.sleep(DISPLAY_INTERVAL)
                
                # Show southbound trains - page 1 (trains 1 & 2)
                line1, line2 = tracker.format_display_lines('south', [0, 1])
                display.write_lines(line1, line2)
                time.sleep(DISPLAY_INTERVAL)
                
                # Show southbound trains - page 2 (train 3)
                line1, line2 = tracker.format_display_lines('south', [2])
                display.write_lines(line1, line2)
                time.sleep(DISPLAY_INTERVAL)
            else:
                # STATIC mode - just sleep and wait for next refresh
                time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        display.write_lines("G Train Display", "Stopped")
        time.sleep(1)
        display.cleanup()
        print("Goodbye!")

if __name__ == "__main__":
    main()