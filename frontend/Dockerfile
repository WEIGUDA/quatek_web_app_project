# build stage
FROM node:10-alpine as build-stage
WORKDIR /app
COPY . /app
RUN npm --registry https://registry.npm.taobao.org install && \
    npm run build

# production stage
FROM nginx:alpine as production-stage
LABEL Name=quatek_web_app_frontend Version=0.0.1
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]