FROM ccr.ccs.tencentyun.com/geekpie/mirrorsimage

MAINTAINER zxt @ Geek Pie Association
RUN mkdir /Mirrors-AutoSync
COPY Mirrors-AutoSync.conf Mirrors-AutoSync.py bandersnatch.conf /Mirrors-AutoSync/
COPY script /Mirrors-AutoSync/script
COPY quick-fedora-mirror.conf /Mirrors-AutoSync/script/
RUN find /Mirrors-AutoSync/script/ -regex '[^\.]*[^/]' | xargs chmod +x
