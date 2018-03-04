FROM ubuntu:18.04

MAINTAINER DEV-GO

RUN apt-get update -y && \
    apt-get install -y \
    nginx \
    python3-dev \
    python3-pip \
    python3-tk \
    libmysqlclient-dev \
    nodejs \
    npm \
    python-software-properties \
	rabbitmq-server \
	software-properties-common


RUN add-apt-repository -y ppa:webupd8team/java && \
    apt-get update && \
    echo "oracle-java8-installer shared/accepted-oracle-license-v1-1 select true" | debconf-set-selections && \
    echo "oracle-java8-installer shared/accepted-oracle-license-v1-1 seen true" | debconf-set-selections && \
    apt-get install -y oracle-java8-installer

# install phantomjs py npm
RUN npm install -g phantomjs-prebuilt

# set locale for ko_KR.UTF-8
RUN locale-gen ko_KR.UTF-8
ENV LANG ko_KR.UTF-8
ENV LANGUAGE ko_KR.UTF-8
ENV LC_ALL ko_KR.UTF-8

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm -rf /etc/nginx/sites-enabled/default
COPY mysite_nginx.conf /etc/nginx/sites-enabled/mysite_nginx.conf
COPY requirements.txt /mysite/

# COPY . /mysite/
VOLUME /mysite/
WORKDIR /mysite/

RUN pip3 install -r requirements.txt

# RUN chmod +x /mysite/docker_start.sh # give permission
# CMD /mysite/docker_start.sh

EXPOSE 80