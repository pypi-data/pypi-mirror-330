from quick_ssh.core.utils import SSHManager


def main():
    ssh_manager = SSHManager()
    ssh_manager.run()

if __name__ == "__main__":
    main()