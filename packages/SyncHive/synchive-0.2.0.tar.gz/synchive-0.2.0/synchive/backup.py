import paramiko
import os
import logging
from datetime import datetime
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)

from .config import load_config

# Configure logging
logging.basicConfig(filename="synchive.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def connect_ssh(config):
    """Establishes an SSH connection."""
    try:
        transport = paramiko.Transport((config["remote_host"], config["port"]))
        
        if config.get("ssh_key"):
            private_key = paramiko.RSAKey(filename=config["ssh_key"])
            transport.connect(username=config["username"], pkey=private_key)
        else:
            transport.connect(username=config["username"], password=config["password"])
        
        return transport
    except Exception as e:
        logging.error(f"SSH connection failed: {e}")
        raise

def create_backup():
    """Creates a zip archive remotely and downloads it locally."""
    config = load_config()
    formatted_datetime = datetime.now().strftime("%d_%m_%y_%H_%M_%S")
    zip_file_name = f"sync_backup_{formatted_datetime}.zip"
    
    try:
        transport = connect_ssh(config)
        sftp = paramiko.SFTPClient.from_transport(transport)
        ssh_client = transport.open_session()
        
        # Create ZIP on remote server using PowerShell
        remote_zip_path = os.path.join(config["remote_path"], zip_file_name)
        powershell_command = f'powershell Compress-Archive -Path "{config["remote_path"]}\\*" -DestinationPath "{remote_zip_path}"'
        ssh_client.exec_command(powershell_command)
        ssh_client.recv_exit_status()

        # Download the ZIP
        local_zip_path = os.path.join(config["local_path"], zip_file_name)
        sftp.get(remote_zip_path, local_zip_path)
        logging.info(f"Backup successful: {local_zip_path}")

        # Remove the ZIP from the remote machine
        sftp.remove(remote_zip_path)

        sftp.close()
        transport.close()
    except Exception as e:
        logging.error(f"Backup failed: {e}")


if __name__ == "__main__":
    create_backup()