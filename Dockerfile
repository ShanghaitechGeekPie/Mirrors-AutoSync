FROM alpine:latest

MAINTAINER zxt @ Geek Pie Association

RUN apk update \
        && apk add --no-cache gcc git python3 musl-dev linux-headers  libc-dev  rsync zsh \
                findutils wget util-linux grep libxml2-dev libxslt-dev \
        #&&  pip3 install --upgrade pip  \
        &&  pip install apscheduler bandersnatch

RUN mkdir /Mirrors-AutoSync

COPY Mirrors-AutoSync.conf Mirrors-AutoSync.py bandersnatch.conf /Mirrors-AutoSync/

COPY script /Mirrors-AutoSync/script
COPY quick-fedora-mirror.conf /Mirrors-AutoSync/script/
RUN find /Mirrors-AutoSync/script/ -regex '[^\.]*[^/]' | xargs chmod +x
RUN find /Mirrors-AutoSync/script/ -regex '[^\.]*\.sh' | xargs chmod +x

RUN mkdir /mirrors/logs -p

CMD python3 /Mirrors-AutoSync/Mirrors-AutoSync.py
