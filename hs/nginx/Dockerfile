FROM nginx

RUN rm /etc/nginx/nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

RUN mkdir -p /etc/nginx/html

COPY nginx.conf /etc/nginx
COPY healthsystem /etc/nginx/html
