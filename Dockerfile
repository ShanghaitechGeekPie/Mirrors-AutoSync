FROM daocloud.io/python:3-onbuild

MAINTAINER eastpiger @ Geek Pie Association

RUN apt-get update && apt-get update && \
	apt-get install -y rsync supervisor
RUN apt-get clean && \
	rm -rf /var/lib/apt/list/*
RUN mkdir /Mirrors-AutoSync
WORKDIR /Mirrors-AutoSync
COPY . /Mirrors-AutoSync
RUN mv supervisor.conf /etc/supervisor/conf.d/
CMD ["supervisor","-n"]
