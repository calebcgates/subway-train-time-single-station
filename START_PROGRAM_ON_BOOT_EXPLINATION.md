# Auto-Start on Boot Configuration

## Overview

The G Train Display is configured to run automatically on Raspberry Pi startup using a **systemd service**. This ensures the display starts immediately when you plug in the Pi, without manual intervention.

## What is systemd?

systemd is Linux's system and service manager. It controls which programs run at boot and manages their lifecycle (start, stop, restart, logs).

## Service Configuration

**Location:** `/etc/systemd/system/gtrain-display.service`

**Key Components:**

- `After=network-online.target` - Waits for network connection before starting
- `WorkingDirectory=/home/pi/nyc-subway` - Sets the working directory
- `ExecStart=/home/pi/nyc-subway/venv/bin/python /home/pi/nyc-subway/display_train.py` - Full path to venv Python (auto-activates virtual environment)
- `Restart=always` - Automatically restarts if the program crashes
- `RestartSec=10` - Waits 10 seconds before restarting

## Setup Commands

```bash
# 1. Create service file
sudo nano /etc/systemd/system/gtrain-display.service

# 2. Reload systemd to recognize new service
sudo systemctl daemon-reload

# 3. Enable service to start on boot
sudo systemctl enable gtrain-display.service

# 4. Start service immediately
sudo systemctl start gtrain-display.service

# 5. Verify it's running
sudo systemctl status gtrain-display.service
```

## Management Commands

```bash
# View live logs
sudo journalctl -u gtrain-display.service -f

# View last 50 log lines
sudo journalctl -u gtrain-display.service -n 50

# Restart service
sudo systemctl restart gtrain-display.service

# Stop service
sudo systemctl stop gtrain-display.service

# Start service
sudo systemctl start gtrain-display.service

# Check service status
sudo systemctl status gtrain-display.service

# Disable auto-start (if needed)
sudo systemctl disable gtrain-display.service
```

## How It Works

1. **Boot**: Raspberry Pi powers on
2. **Network**: systemd waits for network connection
3. **Launch**: Service executes `/home/pi/nyc-subway/venv/bin/python` with the display script
4. **Virtual Environment**: Using the venv's Python binary automatically activates the virtual environment with all dependencies
5. **Monitor**: systemd monitors the process and restarts it if it crashes

## Behavior

- **On Power-Up**: Display starts automatically after 60-90 seconds (boot time + network connection)
- **On Crash**: Automatically restarts after 10 seconds
- **On Manual Stop**: Stays stopped until system reboot or manual start
- **Logs**: All output captured to systemd journal (view with `journalctl`)

## Advantages

- ✅ No manual SSH or commands needed
- ✅ Starts automatically when plugged in
- ✅ Auto-restarts on crashes
- ✅ Logs preserved for debugging
- ✅ Clean start/stop/restart management
- ✅ Works across reboots and power cycles

## Troubleshooting

If service fails to start:

```bash
# Check status and error messages
sudo systemctl status gtrain-display.service

# View detailed logs
sudo journalctl -u gtrain-display.service -n 100

# Test manually to see errors
cd ~/nyc-subway
source venv/bin/activate
python display_train.py
```

Common issues:
- Wrong file paths in service file
- Virtual environment not created or corrupted
- Missing dependencies in venv
- I2C not enabled or LCD not connected
- Network not available (check WiFi configuration)

