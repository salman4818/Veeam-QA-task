import argparse
import os
import time
import shutil
import hashlib
import datetime


def sync_folders(src, dest, interval, log_file):
    while True:
        # Get list of files in source and replica folders
        src_files = set(os.listdir(src))
        dest_files = set(os.listdir(dest))

        # Find files that exist only in the source folder and copy them to the replica folder
        for file in src_files - dest_files:
            shutil.copy(os.path.join(src, file), dest)
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(log_file, 'a') as f:
                f.write(f"Copied {file} from {src} to {dest}\n")
            print(f"Copied {file} from {src} to {dest}")


        # Find files that exist only in the replica folder and delete them
        for file in dest_files - src_files:
            os.remove(os.path.join(dest, file))
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(log_file, 'a') as f:
                f.write(f"Deleted {file} from {dest}\n")
            print(f"Deleted {file} from {dest}")

        # Find files that exist in both folders and compare their contents
        for file in src_files & dest_files:
            src_md5 = calculate_md5(os.path.join(src, file))
            dest_md5 = calculate_md5(os.path.join(dest, file))
            if src_md5 != dest_md5:
                shutil.copy(os.path.join(src, file), dest)
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                with open(log_file, 'a') as f:
                    f.write(f"Updated {file} in {dest}\n")
                print(f"Updated {file} in {dest}")

        time.sleep(interval)

def calculate_md5(file):
    hash_md5 = hashlib.md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('src', help='Path to source folder')
    parser.add_argument('dest', help='Path to replica folder')
    parser.add_argument('--interval', type=int, default=60, help='Synchronization interval in seconds')
    parser.add_argument('--log', dest='log_file', default='sync.log', help='Path to log file')
    args = parser.parse_args()

    sync_folders(args.src, args.dest, args.interval, args.log_file)
