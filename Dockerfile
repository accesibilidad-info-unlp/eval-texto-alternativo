FROM node:24-alpine

WORKDIR /app

RUN addgroup -S app && adduser -S app -G app

COPY package*.json ./

RUN npm ci

COPY . .

RUN mkdir -p /app/_site && chown -R app:app /app

USER app

EXPOSE 8080

CMD ["npx", "eleventy", "--serve"]