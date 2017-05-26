FROM mirrorsimage:latest

MAINTAINER zxt @ Geek Pie Association
RUN mkdir /Mirrors-AutoSync
COPY . /Mirrors-AutoSync
RUN chmod +x /Mirrors-AutoSync/script/*