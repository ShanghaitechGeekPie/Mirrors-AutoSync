FROM daocloud.io/python:3-onbuild

MAINTAINER eastpiger @ Geek Pie Association

RUN mkdir /Mirrors-AutoSync
WORKDIR /Mirrors-AutoSync
COPY . /Mirrors-AutoSync

CMD python3 ./Mirrors-AutoSync.py
