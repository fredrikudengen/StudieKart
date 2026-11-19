# --- dev: Vite dev server with hot reload (used by docker-compose) ---
FROM node:20-alpine AS dev
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]

# --- build: production bundle (reads VITE_API_URL from .env.production) ---
FROM dev AS build
RUN npm run build

# --- production: static files served by nginx (default target) ---
FROM nginx:1.27-alpine
ENV PORT=8080
COPY nginx.conf.template /etc/nginx/templates/default.conf.template
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 8080
