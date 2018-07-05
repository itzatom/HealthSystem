FROM nginx

#RUN rm -r /etc/nginx/conf.d
COPY default.conf /etc/nginx/conf.d/
#RUN nginx -c /etc/nginx/nginx.conf
COPY healthsystem/index.html /usr/share/nginx/html/
