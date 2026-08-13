# SYPHER ENTERPRISE CONTAINERIZATION
# Multi-stage build for Python ML Core, Java Spring Boot, and C++ Native Guards

# Stage 1: Base ML Environment
FROM python:3.10-slim AS ml-core
WORKDIR /app/sypher
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/

# Stage 2: Enterprise Java Integration
FROM amazoncorretto:17-alpine AS enterprise-gateway
WORKDIR /app/sypher-gateway
COPY enterprise_integration/ ./enterprise_integration/

# Stage 3: Production Runtime Assembly
FROM python:3.10-slim
WORKDIR /opt/sypher-production

# Install C++ build tools for native compilation
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY --from=ml-core /app/sypher /opt/sypher-production/ml-engine
COPY --from=enterprise-gateway /app/sypher-gateway /opt/sypher-production/java-gateway
COPY native_cpp/ ./native_cpp/

# Expose Spring Boot REST API port
EXPOSE 8080

# Default execution entrypoint
CMD ["python", "ml-engine/src/training_loop.py"]
