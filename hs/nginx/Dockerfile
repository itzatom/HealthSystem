FROM nginx

<<<<<<< HEAD
RUN rm /etc/nginx/conf.d/default.conf

ADD nginx.conf /etc/nginx/conf.d/default.conf

RUN mkdir -p /etc/nginx/html

COPY healthsystem /usr/share/nginx/html
=======
#RUN rm -r /etc/nginx/conf.d
COPY default.conf /etc/nginx/conf.d/
#RUN nginx -c /etc/nginx/nginx.conf
COPY healthsystem/index.html /usr/share/nginx/html/
>>>>>>> dockerizenginx
