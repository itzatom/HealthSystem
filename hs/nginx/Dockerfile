FROM nginx

RUN rm /etc/nginx/conf.d/default.conf

ADD nginx.conf /etc/nginx/conf.d/default.conf

RUN mkdir -p /etc/nginx/html

COPY healthsystem /usr/share/nginx/html
