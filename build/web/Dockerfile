FROM node:23.7.0 as build

WORKDIR /web
COPY web .
RUN npm install
RUN npm run build


FROM nginx:1.25.5-alpine as runner

# set up a basic configuration
COPY build/web/nginx.conf /etc/nginx/nginx.conf

# copy the dist dir from the vite build
COPY --from=build /web/dist /usr/share/nginx/html
