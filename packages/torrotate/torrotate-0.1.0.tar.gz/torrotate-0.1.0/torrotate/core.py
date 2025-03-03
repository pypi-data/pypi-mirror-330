import platform
import subprocess
import os
import random
import string
import requests as original_requests
import time
import sys
import stem
from stem import Signal
from stem.control import Controller
from stem import SocketError
from stem.connection import MissingPassword
from stem.connection import PasswordAuthFailed

# Configuration and state
_config = {
    'control_port': 9051,
    'control_password': None,
    'rotate_every': 0,
    'requests_since_rotation': 0,
    'proxy_host': '127.0.0.1',
    'proxy_port': 9050,
    'rotation_delay': 3,
    'cookie_auth': False,
    'max_rotation_attempts': 5,
    'last_ip': None,
    'debug': False,
    'force_first_request_rotation': True
}

class TorRequests:
    """A drop-in replacement for requests that routes through Tor with IP rotation"""
    
    def __init__(self):
        self.proxies = {
            'http': f'socks5h://{_config["proxy_host"]}:{_config["proxy_port"]}',
            'https': f'socks5h://{_config["proxy_host"]}:{_config["proxy_port"]}'
        }
    
    def _should_rotate(self):
        if _config['force_first_request_rotation'] and _config['requests_since_rotation'] == 0:
            if _config['debug']:
                print(f"DEBUG: Forcing rotation on first request")
            return True
            
        if _config['rotate_every'] <= 0:
            return False
        
        should_rotate = _config['requests_since_rotation'] >= _config['rotate_every']
        if _config['debug'] and should_rotate:
            print(f"DEBUG: Should rotate IP - requests since last rotation: {_config['requests_since_rotation']}, threshold: {_config['rotate_every']}")
        return should_rotate
    
    def _increment_counter(self):
        _config['requests_since_rotation'] += 1
        if _config['debug']:
            print(f"DEBUG: Request counter incremented to {_config['requests_since_rotation']}")
    
    def _maybe_rotate(self):
        if self._should_rotate():
            if _config['debug']:
                print(f"DEBUG: Rotating IP after {_config['requests_since_rotation']} requests")
            rotate_ip(verbose=_config['debug'], ensure_new_ip=True)
            _config['requests_since_rotation'] = 0
            if _config['debug']:
                print(f"DEBUG: Request counter reset to 0")
        elif _config['debug']:
            print(f"DEBUG: No rotation needed yet. Counter: {_config['requests_since_rotation']}/{_config['rotate_every']}")
    
    def get(self, url, **kwargs):
        self._increment_counter()
        self._maybe_rotate()
        kwargs.setdefault('proxies', self.proxies)
        return original_requests.get(url, **kwargs)
    
    def post(self, url, **kwargs):
        self._increment_counter()
        self._maybe_rotate()
        kwargs.setdefault('proxies', self.proxies)
        return original_requests.post(url, **kwargs)
    
    def put(self, url, **kwargs):
        self._increment_counter()
        self._maybe_rotate()
        kwargs.setdefault('proxies', self.proxies)
        return original_requests.put(url, **kwargs)
    
    def delete(self, url, **kwargs):
        self._increment_counter()
        self._maybe_rotate()
        kwargs.setdefault('proxies', self.proxies)
        return original_requests.delete(url, **kwargs)
    
    def head(self, url, **kwargs):
        self._increment_counter()
        self._maybe_rotate()
        kwargs.setdefault('proxies', self.proxies)
        return original_requests.head(url, **kwargs)

tor_requests = TorRequests()

def _get_torrc_path():
    system = platform.system().lower()
    if system == 'linux':
        paths = ['/etc/tor/torrc', '/usr/local/etc/tor/torrc', '~/.torrc']
    elif system == 'darwin':
        paths = ['/usr/local/etc/tor/torrc', '/opt/homebrew/etc/tor/torrc', '~/.torrc']
    elif system == 'windows':
        paths = [r'C:\Users\All Users\tor\torrc', r'%APPDATA%\tor\torrc']
    else:
        paths = ['/etc/tor/torrc', '~/.torrc']
    
    for path in paths:
        expanded_path = os.path.expanduser(path)
        if os.path.exists(expanded_path):
            return expanded_path
    
    return paths[0]

def configure(tor_control_port=None, tor_control_password=None, 
              proxy_host=None, proxy_port=None, 
              rotate_every=None, rotation_delay=None,
              max_rotation_attempts=None, debug=None,
              force_first_request_rotation=None):

    if tor_control_port is not None:
        _config['control_port'] = tor_control_port
    if tor_control_password is not None:
        _config['control_password'] = tor_control_password
    if proxy_host is not None:
        _config['proxy_host'] = proxy_host
    if proxy_port is not None:
        _config['proxy_port'] = proxy_port
    if rotate_every is not None:
        _config['rotate_every'] = rotate_every
    if rotation_delay is not None:
        _config['rotation_delay'] = max(1, rotation_delay)
    if max_rotation_attempts is not None:
        _config['max_rotation_attempts'] = max(1, max_rotation_attempts)
    if debug is not None:
        _config['debug'] = debug
    if force_first_request_rotation is not None:
        _config['force_first_request_rotation'] = force_first_request_rotation
    
    tor_requests.proxies = {
        'http': f'socks5h://{_config["proxy_host"]}:{_config["proxy_port"]}',
        'https': f'socks5h://{_config["proxy_host"]}:{_config["proxy_port"]}'
    }
    
    if _config['debug']:
        print(f"DEBUG: Configuration updated: rotate_every={_config['rotate_every']}, " +
              f"max_attempts={_config['max_rotation_attempts']}, delay={_config['rotation_delay']}")
    
    _config['requests_since_rotation'] = 0
    
    try:
        _config['last_ip'] = get_current_ip()
        if _config['debug']:
            print(f"DEBUG: Initial IP: {_config['last_ip']}")
        else:
            print(f"Initial IP: {_config['last_ip']}")
        
        result = rotate_ip(verbose=True, ensure_new_ip=False)
        if not result:
            raise RuntimeError("Failed to configure Tor connection")
    except Exception as e:
        print(f"Error rotating IP: {e}")
        configure_tor()
    
def _send_newnym_signal(controller, verbose=False):
    controller.signal(Signal.NEWNYM)
    if verbose:
        print("Tor circuit rotation requested successfully")
    time.sleep(_config['rotation_delay'])

def rotate_ip(verbose=False, ensure_new_ip=True):
    if ensure_new_ip:
        old_ip = _config['last_ip'] if _config['last_ip'] else get_current_ip()
        if verbose:
            print(f"Current IP before rotation: {old_ip}")
    
    try:
        with Controller.from_port(port=_config['control_port']) as controller:
            try:
                if _config['control_password']:
                    controller.authenticate(password=_config['control_password'])
                else:
                    controller.authenticate()
                    if verbose and not _config['cookie_auth']:
                        _config['cookie_auth'] = True
                        print("Note: Using cookie authentication instead of password")
                
            except MissingPassword:
                torrc_path = _get_torrc_path()
                if verbose:
                    print(f"Error: Tor requires a password. Configure it in {torrc_path}")
                return False
                
            except PasswordAuthFailed:
                print(PasswordAuthFailed)
                torrc_path = _get_torrc_path()
                password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
                reset_cmd = f'sudo sh -c \'tor --hash-password "{password}" | tail -n1 | xargs -I {{}} sed -i "s|^HashedControlPassword.*|HashedControlPassword {{}}|" {torrc_path}\''
                if verbose:
                    print(f"Error: Incorrect password.")
                    print("\nIf you forgot your Tor password and want to reset it, run:")
                    print(reset_cmd)
                    print(f"New password would be: {password}")
                    print(f"\nThen simply edit your torrotate.configure parameters with {password} such as")
                    print("import torrotate\ntorrotate.configure(tor_control_password=\"ss\")\nprint(torrotate.requests.get(\"https://httpbin.org/get?word=test123\").text)")
                    print(f"\nThen run sudo systemctl restart tor")
                    sys.exit(1)
                return False
            
            if ensure_new_ip:
                attempts = 0
                max_attempts = _config['max_rotation_attempts']
                new_ip = old_ip
                
                while new_ip == old_ip and attempts < max_attempts:
                    attempts += 1
                    _send_newnym_signal(controller, verbose)
                    new_ip = get_current_ip()
                    
                    if new_ip == old_ip:
                        if verbose:
                            print(f"Attempt {attempts}/{max_attempts}: IP didn't change ({new_ip}), trying again...")
                        time.sleep(1)
                    else:
                        if verbose:
                            print(f"IP successfully changed from {old_ip} to {new_ip} on attempt {attempts}")
                
                _config['last_ip'] = new_ip
                if new_ip == old_ip and attempts >= max_attempts:
                    if verbose:
                        print(f"Warning: Failed to get a new IP after {max_attempts} attempts")
                    return False
                return True
            else:
                _send_newnym_signal(controller, verbose)
                _config['last_ip'] = get_current_ip()
                return True
            
    except SocketError:
        if verbose:
            print(f"Error: Could not connect to Tor control port {_config['control_port']}. Is Tor running?")
        configure_tor()
        return False
        
    except Exception as e:
        if verbose:
            print(f"Error rotating IP: {e}")
        return False

def get_current_ip():
    try:
        response = original_requests.get('https://api.ipify.org?format=json', 
                                         proxies=tor_requests.proxies,
                                         timeout=10)
        return response.json()['ip']
    except Exception as e:
        print(f"Error in torrotate.get_current_ip: {e}")
        return None

def reset_rotation_counter():
    _config['requests_since_rotation'] = 0

def force_new_ip(max_attempts=None, verbose=True):
    if max_attempts is not None:
        old_max = _config['max_rotation_attempts'] 
        _config['max_rotation_attempts'] = max_attempts
        result = rotate_ip(verbose=verbose, ensure_new_ip=True)
        _config['max_rotation_attempts'] = old_max
        return result
    else:
        return rotate_ip(verbose=verbose, ensure_new_ip=True)

def configure_tor():
    check_cmd = lambda cmd: subprocess.run([cmd, '--version'], capture_output=True, text=True).returncode == 0 if subprocess.run([cmd, '--version'], capture_output=True, text=True, errors='ignore') else False
    gen_pass = lambda length=16: ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length))
    get_path = lambda os_type: "/etc/tor/torrc" if os_type == "linux" else "/usr/local/etc/tor/torrc" if os_type == "darwin" else None
    
    def get_ip(use_tor=False):
        try:
            if use_tor:
                proxies = {
                    'http': 'socks5h://127.0.0.1:9050',
                    'https': 'socks5h://127.0.0.1:9050'
                }
                response = original_requests.get('https://api.ipify.org', proxies=proxies, timeout=10)
            else:
                response = original_requests.get('https://api.ipify.org', timeout=10)
            return response.text
        except Exception as e:
            return f"Error getting IP: {str(e)}"

    def is_tor_running():
        if os_type == "linux":
            return subprocess.run(['systemctl', 'is-active', 'tor'], capture_output=True, text=True).stdout.strip() == "active"
        elif os_type == "darwin":
            return subprocess.run(['launchctl', 'list', 'org.torproject.tor'] if check_cmd('launchctl') else ['ps', 'aux'], capture_output=True, text=True).stdout.find('tor') != -1
        return False

    os_type = platform.system().lower()
    print(f"Detected Operating System: {os_type.capitalize()}")

    if not check_cmd('tor'):
        print("\nTor is not installed. Install with:")
        print({"linux": "sudo apt update && sudo apt install tor  # Ubuntu/Debian\nsudo dnf install tor  # Red Hat/Fedora",
               "darwin": "brew install tor  # macOS with Homebrew",
               "windows": "Download from: https://www.torproject.org/download/tor/"}.get(os_type, "Unknown OS"))
        return

    print("Tor is installed!")
    
    if not is_tor_running():
        print("\nTor service is not running. Start it with:")
        if os_type == "linux":
            print("sudo systemctl start tor")
            print("To enable it on boot: sudo systemctl enable tor")
        elif os_type == "darwin":
            print("brew services start tor  # If installed via Homebrew")
            print("or")
            print("tor  # Run directly")
        return
    else:
        print("Tor service is already running!")

    if os_type == "windows":
        print("Automatic configuration not supported on Windows. Configure torrc manually.")
        return

    if not (check_cmd('sed') and check_cmd('grep')):
        print("Required tools (sed/grep) not found. Install with:")
        print({"linux": "sudo apt install sed grep  # Ubuntu/Debian\nsudo dnf install sed grep  # Red Hat/Fedora",
               "darwin": "brew install gnu-sed grep  # macOS with Homebrew"}.get(os_type, "Unknown OS"))
        return

    torrc_path = get_path(os_type)
    if not torrc_path or not os.path.exists(torrc_path):
        print(f"\nCannot find torrc at {torrc_path}. Manual configuration required.")
        return

    try:
        original_ip = get_ip(use_tor=False)
        print(f"\nOriginal IP: {original_ip}")

        has_control_port = subprocess.run(['grep', '^ControlPort', torrc_path], capture_output=True, text=True).stdout.strip()
        has_password = subprocess.run(['grep', '^HashedControlPassword', torrc_path], capture_output=True, text=True).stdout.strip()

        password = gen_pass()
        config_commands = []

        if has_control_port and has_password:
            print("\nTor is already configured with a ControlPort and password!")
        else:
            if not has_control_port:
                config_commands.append(f'echo "ControlPort 9051" >> {torrc_path}')
            else:
                config_commands.append(f'sed -i "s|^ControlPort.*|ControlPort 9051|" {torrc_path}')

            if not has_password:
                config_commands.append(f'tor --hash-password "{password}" | tail -n1 | xargs -I {{}} echo "HashedControlPassword {{}}" >> {torrc_path}')
            else:
                config_commands.append(f'tor --hash-password "{password}" | tail -n1 | xargs -I {{}} sed -i "s|^HashedControlPassword.*|HashedControlPassword {{}}|" {torrc_path}')

            is_root = os.geteuid() == 0 if os.name != 'nt' else False
            if is_root:
                for cmd in config_commands:
                    subprocess.run(['sh', '-c', cmd])
                print("\nTor configuration updated successfully!")
            else:
                sudo_cmd = f"sudo sh -c '{' && '.join(config_commands)}'"
                print("\nScript not run with sudo. Run this command to configure Tor:")
                print(sudo_cmd)
                return

            print(f"Generated password: {password}")
            print("ControlPort set to 9051")
            print(f"Torrc will be updated at: {torrc_path}")

        tor_ip = get_ip(use_tor=True)
        print(f"\nTor IP: {tor_ip}")
        
        if tor_ip != original_ip and "Error" not in tor_ip:
            print("Success! IP changed through Tor.")
        else:
            print("Warning: IP might not have changed or connection failed.")

    except Exception as e:
        print(f"\nConfiguration failed: {str(e)}")
        print(f"Manual configuration:\n1. tor --hash-password {password}")
        print(f"2. Edit {torrc_path} and add:")
        print("   ControlPort 9051")
        print(f"   HashedControlPassword [generated_hash]")

requests = tor_requests

if __name__ == "__main__":
    configure_tor()