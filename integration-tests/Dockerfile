# Systemd inside a Docker container, for CI and local development
ARG BASE_IMAGE=ubuntu:22.04
FROM $BASE_IMAGE

# DEBIAN_FRONTEND is set to avoid being asked for input and hang during build:
# https://anonoz.github.io/tech/2020/04/24/docker-build-stuck-tzdata.html
RUN export DEBIAN_FRONTEND=noninteractive \
 && apt-get update \
 && apt-get install --yes \
        systemd \
        bzip2 \
        curl \
        git \
        sudo \
        python3 \
 && rm -rf /var/lib/apt/lists/*

# Kill all the things we don't need
RUN find /etc/systemd/system \
    /lib/systemd/system \
    -path '*.wants/*' \
    -not -name '*journald*' \
    -not -name '*systemd-tmpfiles*' \
    -not -name '*systemd-user-sessions*' \
    -exec rm \{} \;

RUN systemctl set-default multi-user.target

STOPSIGNAL SIGRTMIN+3

CMD ["/bin/bash", "-c", "exec /lib/systemd/systemd --log-target=journal 3>&1"]
