# Systemd inside a Docker container, for CI only
FROM arm64v8/ubuntu:focal

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update > /dev/null && apt install --yes systemd curl git sudo > /dev/null

# Kill all the things we don't need
RUN find /etc/systemd/system \
    /lib/systemd/system \
    -path '*.wants/*' \
    -not -name '*journald*' \
    -not -name '*systemd-tmpfiles*' \
    -not -name '*systemd-user-sessions*' \
    -exec rm \{} \;

RUN mkdir -p /etc/sudoers.d

RUN systemctl set-default multi-user.target

STOPSIGNAL SIGRTMIN+3

# Uncomment these lines for a development install
ENV TLJH_BOOTSTRAP_DEV=yes
ENV TLJH_BOOTSTRAP_PIP_SPEC=/srv/src
ENV PATH=/opt/tljh/hub/bin:${PATH}

CMD ["/bin/bash", "-c", "exec /lib/systemd/systemd --log-target=journal 3>&1"]
