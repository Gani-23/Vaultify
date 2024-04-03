import os
import shutil
import datetime
import sys
import filecmp

def backup_files(source_dir, destination_dir):
    if not os.path.exists(source_dir):
        print("Source directory does not exist.")
        return

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    files = os.listdir(source_dir)

    for file in files:
        source_file = os.path.join(source_dir, file)
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        destination_file = os.path.join(destination_dir, f"{file}_{timestamp}")

        if os.path.exists(destination_file):
            if filecmp.cmp(source_file, destination_file) and os.path.getmtime(source_file) <= os.path.getmtime(destination_file):
                print(f"Skipping {file} as it already exists and has the same content and a newer modified date.")
                continue

        try:
            shutil.copy2(source_file, destination_file)
            print(f"Successfully backed up {file} to {destination_file}")
        except Exception as e:
            print(f"Failed to backup {file}: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python backup.py /path/to/source /path/to/destination")
    else:
        source_dir = sys.argv[1]
        destination_dir = sys.argv[2]
        backup_files(source_dir, destination_dir)
