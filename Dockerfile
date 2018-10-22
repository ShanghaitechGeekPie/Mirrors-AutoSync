FROM alpine:latest

MAINTAINER zxt @ Geek Pie Association

RUN apk update && apk add --no-cache git python3 rsync zsh findutils wget && pip3 install apscheduler bandersnatch

RUN mkdir /Mirrors-AutoSync

COPY Mirrors-AutoSync.conf Mirrors-AutoSync.py bandersnatch.conf /Mirrors-AutoSync/

COPY script /Mirrors-AutoSync/script
COPY quick-fedora-mirror.conf /Mirrors-AutoSync/script/
RUN find /Mirrors-AutoSync/script/ -regex '[^\.]*[^/]' | xargs chmod +x
RUN find /Mirrors-AutoSync/script/ -regex '[^\.]*\.sh[^/]' | xargs chmod +x

CMD python3 /Mirrors-AutoSync/Mirrors-AutoSync.py
