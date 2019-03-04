# build stage
FROM node:10 as build-stage
WORKDIR /app
COPY . /app
RUN npm install
# RUN npm install 
RUN ["npm", "run", "build"]


# production stage
FROM nginx:alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]