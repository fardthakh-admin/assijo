FROM nginx:1.24.0-alpine

WORKDIR /app/nginx

COPY ./docker/nginx/production /etc/nginx/conf.d


CMD ["nginx", "-g", "daemon off;"]