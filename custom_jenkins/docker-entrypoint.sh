#!/bin/bash
set -e

# Switch to root temporarily
if [ "$(id -u)" = "0" ]; then
    # Ensure docker group exists
    groupadd -f docker
    usermod -aG docker jenkins || true

    # If docker.sock exists, fix permissions
    if [ -S /var/run/docker.sock ]; then
        chown root:docker /var/run/docker.sock
        chmod 660 /var/run/docker.sock
    fi

    # Drop back to Jenkins user
    exec su -s /bin/bash jenkins -c "/usr/local/bin/jenkins.sh"
else
    # If already Jenkins, just start Jenkins normally
    exec /usr/local/bin/jenkins.sh
fi
