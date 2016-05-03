FROM daocloud.io/python:3-onbuild

MAINTAINER eastpiger @ Geek Pie Association

RUN apt-get update && apt-get update && \
	apt-get install -y rsync supervisor
RUN apt-get clean && \
	rm -rf /var/lib/apt/list/*
RUN mkdir /Mirrors-AutoSync
WORKDIR /Mirrors-AutoSync
COPY . /Mirrors-AutoSync
RUN chmod +x /Mirrors-AutoSync/script/*
RUN mv supervisor.conf /etc/supervisor/conf.d/

RUN mkdir ~/bin && PATH=~/bin:$PATH && curl https://storage-googleapis.lug.ustc.edu.cn/git-repo-downloads/repo > ~/bin/repo && chmod a+x ~/bin/repo

CMD ["supervisor","-n"]
