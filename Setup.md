# Step-by-Step Setup Guide

Follow these instructions to set up the Django Fullstack application locally, via Docker, or on Kubernetes.

## 1. Local Development Setup

### Prerequisites
- Python 3.12+
- PostgreSQL (or use the default SQLite for quick testing)
- Redis (for Celery/Channels)

### Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/lightsspeed/Django-Fullstack-DevsecOps-and-Kubernetes-Deployment.git
   cd Django-Fullstack-DevsecOps-and-Kubernetes-Deployment
   ```

2. **Create Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in the root:
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key
   DATABASE_URL=sqlite:///db.sqlite3
   ```

4. **Run Migrations & Start**:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

---

## 2. Docker Setup

1. **Build the Image**:
   ```bash
   docker build -t django-app .
   ```

2. **Run the Container**:
   ```bash
   docker run -p 8000:8000 --env-file .env django-app
   ```

---

## 3. Kubernetes Deployment

### Prerequisites
- A running K8s cluster (Minikube, Kind, or Managed Service)
- `kubectl` configured

### Steps
1. **Apply Infrastructure (Postgres & Redis)**:
   ```bash
   kubectl apply -f kubernetes/infrastructure.yaml
   ```

2. **Apply Configuration & Secrets**:
   > [!IMPORTANT]
   > Update `kubernetes/config.yaml` with your actual secrets before applying.
   ```bash
   kubectl apply -f kubernetes/config.yaml
   ```

3. **Deploy the Application**:
   ```bash
   kubectl apply -f kubernetes/django-deployment.yaml
   ```

4. **Verify**:
   ```bash
   kubectl get pods
   kubectl get svc django-service
   ```

---

## 4. Monitoring & Logging Setup

The monitoring stack is designed to run via Docker Compose for simplicity.

1. **Start the Stack**:
   ```bash
   cd monitoring
   docker-compose up -d
   ```

2. **Access Dashboards**:
   - **Grafana**: http://localhost:3000 (Login: `admin` / `admin`)
   - **Prometheus**: http://localhost:9090

3. **Business Metrics**:
   View metrics directly from the app at: `http://localhost:8000/metrics`

---

## 5. CI/CD Workflow

The GitHub Actions workflow is automatically triggered on:
- Pushes to `main`/`master`
- Pull Requests to `main`/`master`

It performs **Linting**, **SAST (Bandit)**, **SCA (Safety/Trivy)**, and **Container Scanning**. Check the "Actions" tab in your GitHub repository to see the results.
