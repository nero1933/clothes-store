FROM node:21-alpine

LABEL maintainer="nero"

WORKDIR /ui

COPY package.json ./

RUN npm install

COPY . .

EXPOSE 3000

CMD [ "npm", "run", "dev" ]
