# QR Code Generator Service

A scalable QR code generation service with caching and expiration support.

## High-Level Design

### Architecture Components

- **FastAPI Application**: REST API for QR code generation and retrieval
- **PostgreSQL**: Stores QR code metadata and relationships
- **Redis Cache**: Improves retrieval performance for frequent requests
- **Celery Worker**: Handles background tasks (cleanup of expired codes)
- **Docker**: Containerization for consistent deployment

### System Flow
```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Client    │ ─────► │   FastAPI    │ ─────► │   Redis     │
└─────────────┘         └─────────────┘         └─────────────┘
                              │                        ▲
                              ▼                        │
                        ┌─────────────┐         ┌─────────────┐
                        │ PostgreSQL  │ ◄────── │   Celery    │
                        └─────────────┘         └─────────────┘
```

## Installation & Setup

### Prerequisites
- Docker and Docker Compose
- Python 3.10+ (for local development)

### Local Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd qr-code-generator
```

2. Create environment files:
```bash
cp .env.example .env
```

3. Start the services:
```bash
docker-compose up --build
```

## API Documentation

### Generate QR Code
**Endpoint**: `POST /generate`

Request:
```json
{
    "data": "https://example.com",
    "expiration_hours": 24
}
```

Response:
```json
{
    "qr_id": "550e8400-e29b-41d4-a716-446655440000",
    "expires_at": "2024-01-22T15:30:00Z"
}
```

### Retrieve QR Code
**Endpoint**: `GET /retrieve/{qr_id}`

Response:
```json
{
    "qr_code": "/app/qr_codes/550e8400-e29b-41d4-a716-446655440000.png"
}
```

## Deployment Guide

### Production Deployment

1. Configure production environment:
```bash
cp .env.example .env.prod
```
Edit `.env.prod` with your production credentials.

2. Update Docker Hub credentials:
```bash
export DOCKER_USERNAME=your-username
export TAG=latest
```

3. Deploy using the deployment script:
```bash
chmod +x deploy.sh
./deploy.sh
```

### Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_HOST`: Redis server hostname
- `REDIS_PORT`: Redis server port
- `CELERY_BROKER_URL`: Celery broker URL
- `DB_PASSWORD`: Database password
- `RESTART_POLICY`: Container restart policy
- `DOCKER_USERNAME`: Docker Hub username
- `TAG`: Docker image tag

### Monitoring

- PostgreSQL logs: `docker-compose logs postgres`
- Application logs: `docker-compose logs web`
- Celery worker logs: `docker-compose logs celery_worker`

### Maintenance

Cleanup expired QR codes:
- Automatic cleanup runs every hour
- Manual cleanup: `docker-compose exec celery_worker celery -A src.celery_tasks.tasks cleanup_expired_codes`

## Security Considerations

- Use secure passwords in production
- Configure proper firewall rules
- Regular security updates
- Implement rate limiting for API endpoints
- Use HTTPS in production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License
