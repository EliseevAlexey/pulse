FROM node:20-alpine AS builder
WORKDIR /app

COPY frontend/package.json frontend/yarn.lock ./
RUN yarn install

COPY frontend/.env.docker .env
COPY frontend/ .

RUN yarn build --mode docker

FROM nginx:stable-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]
