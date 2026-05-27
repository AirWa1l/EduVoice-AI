### Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Build arguments
ARG VITE_API_URL
ARG VITE_GOOGLE_CLIENT_ID
ARG VITE_APP_ENV
ARG VITE_DEBUG

# Convert build args to env vars for Vite
ENV VITE_API_URL=$VITE_API_URL
ENV VITE_GOOGLE_CLIENT_ID=$VITE_GOOGLE_CLIENT_ID
ENV VITE_APP_ENV=$VITE_APP_ENV
ENV VITE_DEBUG=$VITE_DEBUG

COPY package.json package-lock.json ./
COPY index.html ./
COPY public ./public
COPY src ./src
COPY vite.config.js ./

RUN npm ci --silent

RUN npm run build


### Production stage
FROM nginx:stable-alpine

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]