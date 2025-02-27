
## Available Commands

---
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


---

## Examples

1. Adding new server
```bash
ssh-manager > add
Enter a name for this connection: webserver
Enter hostname: example.com
Enter username: admin
Enter port (default: 22): 22
```
2. See store connections
```bash
quick-ssh > list
Saved SSH Connections:
--------------------------------------------------
Name: test-host-1
Host: 127.0.0.1
User: local
Port: 22
--------------------------------------------------
Name: test-host-2
Host: 127.0.0.1
User: local
Port: 22
```

3. Check status of server, by default all servers are checked, you can also pass specific server.
```bash
quick-ssh > status
Available connections:
- test-host
- dev-host-idp
- dev-host

Enter server name to check (press Enter to check all): test-host
Checking server status...
--------------------------------------------------
Server: test-host
Host: 127.0.0.1
Ping: ✓ (49.6ms)
SSH (Port 22): ✗
Status: OFFLINE

```


---
[//]: # (## Configuration)

[//]: # ()
[//]: # (- Credentials are stored in `~/.ssh_manager/credentials.json`)

[//]: # (- Session logs are saved in the application directory)

[//]: # (- Command history is maintained in `~/.ssh_manager/history`)

## Requirements

- Python 3.11+

[//]: # (- Internet connection for public IP lookup and server status checks)

## License

[MIT License](LICENSE)

## Acknowledgments
- OpenSSH project
- Python community
- Contributors and testers

## Support
- For support, please open an issue in the GitHub repository or contact the maintainers.

## Roadmap
- [ ] Implement encrypted password storage
- [ ] Add support for SSH key management
- [ ] Integrate with cloud providers
- [ ] Add batch operation support
- [ ] Implement server grouping