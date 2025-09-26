# Use the Jenkins LTS image as base
FROM jenkins/jenkins:lts

# Switch to root
USER root

# Install Docker CLI inside Jenkins container
RUN apt-get update -y && \
    apt-get install -y apt-transport-https ca-certificates curl gnupg software-properties-common && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
    echo "deb [arch=amd64] https://download.docker.com/linux/debian bullseye stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update -y && \
    apt-get install -y docker-ce docker-ce-cli containerd.io && \
    apt-get clean

# Add jenkins user to docker group
RUN groupadd -f docker && usermod -aG docker jenkins

# Add startup script for fixing docker.sock permissions
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Switch back to Jenkins user by default
USER jenkins

# Use our custom entrypoint to fix docker.sock at runtime
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
