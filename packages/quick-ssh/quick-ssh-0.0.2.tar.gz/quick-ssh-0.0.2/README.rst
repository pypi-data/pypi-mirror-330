
### Available Commands

- `add` - Add new SSH server credentials
- `list` - View all saved connections
- `connect` - Connect to a saved server
- `remove` - Delete saved credentials
- `edit` - Modify existing credentials
- `status` - Check server availability
- `ip` - Display local and public IP addresses
- `history` - View command history
- `clear` - Clear screen
- `help` - Show all available commands
- `exit` - Close the application

## Configuration

- Credentials are stored in `~/.ssh_manager/credentials.json`
- Session logs are saved in the application directory
- Command history is maintained in `~/.ssh_manager/history`

## Requirements

- Python 3.6+
- SSH client installed on your system
- Internet connection for public IP lookup and server status checks

## License

[MIT License](LICENSE)