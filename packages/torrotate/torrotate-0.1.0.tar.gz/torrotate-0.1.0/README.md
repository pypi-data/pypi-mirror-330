# TorRotate

A drop-in replacement for the Python `requests` library that routes traffic through Tor with automatic IP rotation.

## Features

- Seamless drop-in replacement for the requests library
- Automatic IP rotation based on request count
- Manual IP rotation available when needed
- Configure Tor directly from Python
- Cross-platform support (Linux, macOS, Windows with limitations)

## Installation

```bash
pip install torrotate
```

## Requirements

- Python 3.7+
- Tor service installed and running
- Tor control port enabled and accessible

## Quick Start

```python
import torrotate

# Configure with default settings
torrotate.configure()

# Make requests through Tor
response = torrotate.requests.get("https://api.ipify.org?format=json")
print(f"Current IP: {response.json()['ip']}")

# Force IP rotation
torrotate.force_new_ip()

# Make another request with new IP
response = torrotate.requests.get("https://api.ipify.org?format=json")
print(f"New IP: {response.json()['ip']}")
```

## Advanced Configuration

Make sure you specify tor_control_password in your script before using torrotate.requests
```python
import torrotate

torrotate.configure(tor_control_password="LFbEWR4Vecek9xif")

print(torrotate.requests.get("https://httpbin.org/get?word=test123").text)
```

```python
torrotate.configure(
    tor_control_port=9051,                # Tor control port number
    tor_control_password="your_password", # Password for Tor control port
    proxy_host="127.0.0.1",               # Tor SOCKS proxy host
    proxy_port=9050,                      # Tor SOCKS proxy port
    rotate_every=10,                      # Rotate IP every 10 requests
    rotation_delay=3,                     # Wait 3 seconds after rotation
    max_rotation_attempts=5,              # Try up to 5 times to get a new IP
    debug=True                            # Enable verbose output
)
```

## Setting Up Tor

On Debian/Ubuntu:

```bash
sudo apt install tor
sudo systemctl start tor
sudo systemctl enable tor
```

Edit the Tor configuration file:

```bash
sudo nano /etc/tor/torrc
```

Add these lines:

```
ControlPort 9051
HashedControlPassword 16:01234567890ABCDEF...
```

To generate a hashed password:

```bash
tor --hash-password "your_password"
```

Restart Tor:

```bash
sudo systemctl restart tor
```

## API Reference

### Main Functions

- `configure()` - Set up the TorRotate library
- `requests` - Drop-in replacement for the requests library
- `force_new_ip()` - Force rotation to a new IP address
- `get_current_ip()` - Get the current external IP address
- `reset_rotation_counter()` - Reset the request counter
- `rotate_ip()` - Rotate to a new Tor circuit
- `configure_tor()` - Interactive Tor configuration helper