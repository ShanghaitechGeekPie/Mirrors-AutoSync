FROM mirrorsimage:latest

MAINTAINER zxt @ Geek Pie Association
RUN mkdir /Mirrors-AutoSync
COPY Mirrors-AutoSync.conf Mirrors-AutoSync.py bandersnatch.conf /Mirrors-AutoSync/
COPY script /Mirrors-AutoSync/script
RUN find /Mirrors-AutoSync/script/ -regex '[^\.]*[^/]' | xargs chmod +x