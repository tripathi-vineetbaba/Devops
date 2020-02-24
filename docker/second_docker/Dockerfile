FROM ubuntu
RUN apt-get update && \
    apt install -y python3 && \
    apt install -y apache2 && \
    apt install -y ufw && \
    ufw allow 'Apache Full' && \
    ufw allow 80/tcp
ADD hello_world.py /root/
ADD index.html /var/www/http/
RUN service apache2 stop
RUN service apache2 start
EXPOSE 80
ENTRYPOINT ["python3","/root/hello_world.py"]
