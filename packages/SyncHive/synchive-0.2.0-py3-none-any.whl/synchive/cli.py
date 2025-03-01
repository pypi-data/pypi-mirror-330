import argparse
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)

from backup import create_backup

def main():
    parser = argparse.ArgumentParser(description="SyncHive: Automated File Backup Utility")
    parser.add_argument("--backup", action="store_true", help="Run the backup process")
    
    args = parser.parse_args()

    if args.backup:
        create_backup()

if __name__ == "__main__":
    main()
