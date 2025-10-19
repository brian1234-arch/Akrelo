# Stage 1: build frontend
FROM node:18-alpine as node_builder
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# Stage 2: python backend
FROM python:3.11-slim
WORKDIR /app
# system deps
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
# copy backend
COPY backend/ backend/
# copy built frontend
COPY --from=node_builder /app/frontend/dist backend/static
# python deps
WORKDIR /app/backend
RUN pip install --no-cache-dir fastapi uvicorn[standard] pandas openpyxl filelock python-multipart
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
# run uvicorn; it will serve api on 8000 and static files on 3000 via a small static server
CMD ["sh","-c","uvicorn app.main:app --host 0.0.0.0 --port 8000"]
