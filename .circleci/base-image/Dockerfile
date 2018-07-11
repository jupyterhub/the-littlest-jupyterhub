FROM continuumio/miniconda3:4.5.4


RUN apt-get update --yes

RUN apt-get install --yes --no-install-recommends \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg2 \
        software-properties-common

RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -

RUN add-apt-repository \
        "deb [arch=amd64] https://download.docker.com/linux/debian \
        $(lsb_release -cs) \
        stable"

RUN apt-get update --yes

RUN apt-get install --yes  docker-ce
