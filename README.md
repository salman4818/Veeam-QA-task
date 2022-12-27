This script synchronizes the contents of a source folder with a replica folder. It does this by continuously checking the contents of both folders and performing the following actions:

Copying files from the source folder to the replica folder if they don't exist in the replica folder
Deleting files from the replica folder if they don't exist in the source folder
Updating the contents of files in the replica folder if their contents differ from the corresponding file in the source folder
The script can be run from the command line with the following arguments:

src: Path to the source folder

dest: Path to the replica folder

--interval (optional): Synchronization interval in seconds. Default is 60 seconds.

--log (optional): Path to the log file. Default is sync.log.

To run the script, enter the following command:



`python sync_folders.py src dest [--interval INTERVAL] [--log LOG_FILE]`
