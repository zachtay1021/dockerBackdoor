# dockerBackdoor
Using docker to create a reverse shell on the host system


## Prerequisite
This script works by utilizing the docker daemon to send docker commands remotely. The target machine must have the docker daemon enabled and listening for TCP connections. By default, this feature of Docker is disabled. If the daemon is not enabled, this script will not work.

Host machine needs Python3 & docker python library

## How to use
The script connects to the docker socket of the target's system and creates a privileged docker container. It escapes the container by connecting back to a netcat listener (by default set to port 4443).

Set up a NC listener and run the script
- nc -lvnp 4443
- python3 dockerBackdoor.py
