# Django Fullstack DevSecOps & Kubernetes Deployment

![Django](https://img.shields.io/badge/django-%23092e20.svg?style=for-the-badge&logo=django&logoColor=white)
![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=Prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/grafana-%23F46800.svg?style=for-the-badge&logo=grafana&logoColor=white)

A production-ready Django application integrated with modern DevSecOps practices, Kubernetes orchestration, and a comprehensive monitoring stack.

## 🚀 Features

- **Fullstack Django**: Real-time polling and voting application.
- **Containerization**: Optimized multi-stage Docker build.
- **Orchestration**: Kubernetes manifests for Django, PostgreSQL, and Redis.
- **DevSecOps CI/CD**: 
  - Linting (Black, Flake8)
  - SAST (Bandit)
  - SCA (Safety, Trivy FS)
  - Container Scanning (Trivy Image)
- **Monitoring & Logging**:
  - Prometheus for system and business metrics.
  - Grafana with pre-configured data sources.
  - Promtail/Loki for log aggregation.
- **Business Metrics**: Custom metrics tracking total votes cast.

## 📁 Repository Structure

```text
├── .github/workflows/    # CI/CD Pipeline
├── kubernetes/           # K8s Manifests (Deployment, Service, Config)
├── monitoring/           # Prometheus, Grafana, Promtail configs
├── polls/                # Polls Application logic
├── users/                # User Management logic
├── voting_project/       # Project Configuration
├── Dockerfile            # Multi-stage Docker build
├── requirements.txt      # Python Dependencies
└── Setup.md              # Detailed Setup Guide
```

## 🛠️ Quick Start

For detailed instructions, see **[Setup.md](Setup.md)**.

### Local Development
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Run with Docker
```bash
docker build -t django-app .
docker run -p 8000:8000 django-app
```

### Monitoring Stack
```bash
cd monitoring
docker-compose up -d
```

## 🛡️ DevSecOps Principles

This project implements:
1. **Shifting Left**: Security scans run on every pull request.
2. **Infrastructure as Code**: Kubernetes manifests and Dockerfiles are version-controlled.
3. **Least Privilege**: Application runs as a non-root user in Docker.
4. **Visibility**: Real-time monitoring and logging for operational security.

## 📄 License

This project is open-source and available under the MIT License.
