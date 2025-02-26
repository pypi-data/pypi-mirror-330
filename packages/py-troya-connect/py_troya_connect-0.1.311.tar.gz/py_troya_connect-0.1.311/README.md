# py-troya-connect

'py-troya-connect' is a framework for terminal screen communication between environment and supporting terminals listed below. 
* Attachmate Extra! X-treme
* Host Integration Server 2000
* NetManage 3270.

## Installation

```bash
pip install py-troya-connect
```

## Quick Start

```python
from py_troya_connect import ExtraTerminal, TerminalType

# Basic connection
terminal = ExtraTerminal("1")  # Connect to first session
terminal.connect()

# Send a command and read response
terminal.send_command("A10JANISTESB")
screen = terminal.read_screen()
print(screen)

terminal.disconnect()
```

## Examples

### 1. Multiple Terminal Types

- Multiple terminal type support (Attachmate Extra! X-treme, Host Integration Server 2000, NetManage 3270)

```python
# Let user see avaliable terminal options
available_types = ExtraTerminal.detect_terminal_type()
available_types

# Choose first possible terminal type with session number 1 
terminal = ExtraTerminal("1", terminal_type=available_types[0])
terminal.connect()
```

### 2. Session Management

```python
# List available sessions
sessions = terminal.list_available_sessions()
print(f"Available sessions: {sessions}")

# Select among terminals listed
terminal = ExtraTerminal("1")
```

### 3. Screen Operations

```python
# Read screen with different options
raw_screen = terminal.read_screen(strip_whitespace=False)
formatted_screen = terminal.read_screen(strip_whitespace=True)

# Wait for specific text
if terminal.wait_for_text("READY", timeout=30):
    print("System is ready")
```

### 4. Command Handling

```python
# Send commands with special keys
terminal.send_command("LOGON USERID{TAB}PASSWORD")
terminal.send_command("CLEAR", wait_for_text="Ready")

# Format commands automatically
terminal.send_command("PF3")  # Automatically adds <ENTER>
```

### 5. Error Handling

```python
from py_troya_connect import ExtraTerminalError, ConnectionError

try:
    terminal = ExtraTerminal("1")
    terminal.connect()
    terminal.send_command("invalid_command")
except ConnectionError as e:
    print(f"Connection failed: {e}")
except ExtraTerminalError as e:
    print(f"Terminal error: {e}")
```

### 6. System Status

```python
# Check system status
terminal = ExtraTerminal("1")
status = terminal.check_system_status()

print(f"Terminal version: {status['Terminal Version']}")
print(f"Active sessions: {status['Session Count']}")
```

## Advanced Features

- Automatic terminal detection
- Robust error handling
- Screen content parsing
- Command formatting
- Session management
- System diagnostics

## Requirements

- Windows OS
- One of the following terminals:
  - Attachmate Extra! Terminal
  - Microsoft HIS 2000
  - NetManage 3270 Client
- Python 3.6+
- pywin32

## License

MIT License
