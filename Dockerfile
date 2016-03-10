FROM debian:jessie

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update && \
    apt-get -y install \
    git \
    python \
    python-pip \
    python-requests \
    supervisor

ADD resources/supervisor/supervisord.conf /etc/supervisor/supervisord.conf
CMD /usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf

RUN pip install git+https://github.com/gomezsan/ochopod.git
RUN apt-get remove -y git

RUN apt-get -y autoremove  && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
