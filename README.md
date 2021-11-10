# dockerBackdoor
Using docker as a backdoor


## Prerequisite
This script works by exploiting the docker socket. The target machine must have the docker socket enabled and listening for TCP connections. By default, this feature of Docker is disabled. If the socket is not open, this script will not work.

Host machine needs Python3 & docker python library
>> pip install docker

## How to use
The script connects to the docker socket of the target's system and creates a privileged docker container. It escapes the container by connecting back to a netcat listener (by default set to port 4443).

Set up a NC listener and run the script
>> nc -lvnp 4443
>> python3 dockerBackdoor.py
