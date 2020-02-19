FROM ubuntu
RUN apt-get update && \
    apt-get install -y apache2 && \
    apt-get install -y ufw
    apt-get install -y vim
RUN service apache2 start
LABEL maintainer=Vineet
COPY docker/index.html /var/www/html/
