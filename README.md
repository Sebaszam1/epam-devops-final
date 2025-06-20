# DevOps Final Project - Python FastAPI Application

A Python application developed with FastAPI and Domain Driven Design (DDD) architecture, deployed on AWS EKS using GitOps and Infrastructure as Code.

## 📋 Table of Contents

- [Architecture](#-architecture)
- [Setup and Installation](#-setup-and-installation)
- [CI/CD Pipelines](#-cicd-pipelines)
- [Project Structure](#-project-structure)
- [Local Usage](#-local-usage)
- [Testing](#-testing)
- [DDD Principles](#-ddd-principles)

## 🏗️ Architecture

### Overall System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GitHub Repo   │    │   GitHub Actions │    │      AWS        │
│                 │    │                  │    │                 │
│ ┌─────────────┐ │    │ ┌──────────────┐ │    │ ┌─────────────┐ │
│ │    App/     │─├────┤→│  App Pipeline │─├────┤→│   EKS       │ │
│ │  FastAPI    │ │    │ │  - Build      │ │    │ │  Cluster    │ │
│ │             │ │    │ │  - Test       │ │    │ │             │ │
│ └─────────────┘ │    │ │  - Deploy     │ │    │ └─────────────┘ │
│                 │    │ └──────────────┘ │    │                 │
│ ┌─────────────┐ │    │                  │    │ ┌─────────────┐ │
│ │   Infra/    │─├────┤┐ ┌──────────────┐│    │ │   VPC       │ │
│ │ Terraform   │ │    ││ │ Infra Pipeline││    │ │ Load Balancer│ │
│ │             │ │    │└→│  - Plan       ││    │ │   ELB       │ │
│ └─────────────┘ │    │  │  - Apply      ││    │ └─────────────┘ │
└─────────────────┘    │  └──────────────┘│    └─────────────────┘
                       └──────────────────┘
```

### Infrastructure Architecture (AWS)

- **VPC**: Virtual private cloud with public and private subnets
- **EKS Cluster**: Managed Kubernetes with nodes in private subnets
- **Application Load Balancer**: Load balancer for external access
- **NAT Gateway**: For internet access from private subnets
- **IAM Roles**: Granular policies for services and workloads

### Application Architecture (DDD)

```
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI Application                     │
├─────────────────────────────────────────────────────────────┤
│  Infrastructure Layer (controllers.py)                     │
│  ├─ REST API Endpoints                                      │
│  └─ HTTP Handlers                                           │
├─────────────────────────────────────────────────────────────┤
│  Application Layer (use_cases.py)                          │
│  ├─ Business Logic Orchestration                           │
│  └─ Use Cases Implementation                                │
├─────────────────────────────────────────────────────────────┤
│  Domain Layer (entities.py, repositories.py)               │
│  ├─ Business Entities                                       │
│  ├─ Domain Rules                                            │
│  └─ Repository Interfaces                                   │
└─────────────────────────────────────────────────────────────┘
```

## ⚙️ Setup and Installation

### Prerequisites

- **Local Tools:**
  - Python 3.11+
  - Docker
  - kubectl
  - AWS CLI
  - Terraform 1.5+

- **Cloud Services:**
  - AWS account with administrative permissions
  - Docker Hub account
  - GitHub repository with Actions enabled

### Environment Variables and Secrets

#### GitHub Secrets (Required)
```bash
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
DOCKERHUB_USERNAME=your_dockerhub_username
DOCKERHUB_TOKEN=your_dockerhub_token
AWS_ACCOUNT_ID=your_aws_account_id  # Optional, default: 928558117008
```

#### GitHub Variables (Optional)
```bash
PROJECT_NAME=epam-devops-final  # Default value
AWS_REGION=us-east-1           # Default value
```

### Initial Setup

#### 1. Clone Repository
```bash
git clone <repository-url>
cd DevOps-Final-Project
```

#### 2. Configure AWS CLI
```bash
aws configure
# Enter AWS Access Key ID
# Enter AWS Secret Access Key
# Region: us-east-1
# Format: json
```

#### 3. Configure Terraform Backend (Optional)
```bash
cd infra/
# Edit backend.tf with your S3 bucket and DynamoDB table
# Or comment out to use local backend
```

#### 4. Manual Deploy (Alternative to Pipelines)

**Infrastructure:**
```bash
cd infra/
terraform init
terraform plan
terraform apply
```

**Application:**
```bash
# Build and push Docker image
cd app/
docker build -t your-repo/app:latest .
docker push your-repo/app:latest

# Configure kubectl
aws eks update-kubeconfig --region us-east-1 --name epam-devops-final-eks

# Deploy application
kubectl apply -f ../k8s/
```

## 🚀 CI/CD Pipelines

### Infrastructure Pipeline (.github/workflows/infra.yml)

**Trigger:** Changes in `infra/` or pipeline file

**Flow:**
1. **Setup:** Terraform installation
2. **Validate:** Syntax validation
3. **Plan:** Infrastructure planning
4. **Apply:** Infrastructure deployment

**Resources Created:**
- VPC with public/private subnets
- EKS Cluster (v1.29)
- Node Groups (t3.small)  
- IAM Roles for Load Balancer Controller
- Security Groups and necessary policies

### Application Pipeline (.github/workflows/app.yml)

**Trigger:** Changes in `app/`

**Phases:**

#### 1. Build & Test
- Setup Python 3.11
- Install dependencies
- Run unit tests with coverage
- Generate test reports

#### 2. Docker Build & Push
- Build multi-stage Docker image
- Security scanning
- Push to Docker Hub registry
- Image vulnerability assessment

#### 3. Infrastructure Setup
- Configure AWS credentials
- Update kubeconfig
- Verify cluster connectivity
- Wait for cluster readiness

#### 4. Load Balancer Setup
- Install Helm
- Add AWS EKS Charts repository
- Deploy AWS Load Balancer Controller
- Configure IAM Service Account
- Wait for controller readiness

#### 5. Application Deployment
- Apply ConfigMap
- Deploy application (2 replicas)
- Create Service (ClusterIP)
- Configure Ingress (ALB)
- Rolling update strategy
- Health checks validation

**Deployment Strategies:**
- Rolling updates (zero-downtime)
- Health checks (readiness/liveness probes)
- Resource limits and requests
- Horizontal Pod Autoscaling ready

### Monitoring and Observability

**Health Checks:**
- Container health checks
- Kubernetes readiness probes
- Load balancer health checks
- Application health endpoints

**Logging:**
- Structured logging with Python logging
- Container logs via kubectl
- CloudWatch integration (EKS)

## 📁 Project Structure

```
DevOps-Final-Project/
├── app/                           # Application code
│   ├── main.py                   # FastAPI entry point
│   ├── Dockerfile                # Multi-stage container build
│   ├── requirements.txt          # Python dependencies
│   ├── domain/                   # DDD domain layer
│   │   ├── entities.py          # Business entities
│   │   └── repositories.py      # Repository interfaces
│   ├── application/              # DDD application layer
│   │   └── use_cases.py         # Use cases
│   └── infrastructure/           # DDD infrastructure layer
│       ├── controllers.py       # FastAPI endpoints
│       └── repositories.py      # Implementations
├── infra/                        # Infrastructure as Code
│   ├── main.tf                  # Main resources (VPC, EKS)
│   ├── variables.tf             # Input variables
│   ├── outputs.tf               # Outputs (cluster info, etc.)
│   ├── versions.tf              # Provider versions
│   ├── backend.tf               # Remote state backend
│   ├── terraform.tfvars         # Variable values
│   └── iam-policy.json          # IAM policies
├── k8s/                          # Kubernetes manifests
│   ├── deployment.yaml          # Deployment with 2 replicas
│   ├── service.yaml             # ClusterIP Service
│   ├── ingress.yaml             # ALB Ingress
│   └── configmap.yaml           # Configuration variables
├── .github/workflows/            # CI/CD pipelines
│   ├── app.yml                  # Application pipeline
│   └── infra.yml                # Infrastructure pipeline
├── tests/                        # Unit and integration tests
└── requirements.txt              # Testing dependencies
```

## 💻 Local Usage

### Local Development

#### 1. Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r app/requirements.txt
```

#### 2. Run Application
```bash
cd app/
python main.py
```

The application will be available at:
- **API:** http://localhost:8000
- **Documentation:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

#### 3. Testing with Docker
```bash
# Build locally
docker build -t local-app ./app

# Run container
docker run -p 8000:8000 local-app
```

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/health` | Health check with metadata |
| GET | `/api/v1/health` | Simple health check |
| GET | `/api/v1/user/{username}` | User information |

### Usage Examples

```bash
# Health check
curl http://localhost:8000/health

# Specific user
curl http://localhost:8000/api/v1/user/sebas

# Interactive documentation
open http://localhost:8000/docs
```

## 🧪 Testing

### Run Tests

```bash
# Install testing dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Tests with coverage
pytest --cov=app --cov-report=html --cov-report=term-missing

# Specific tests by layer
pytest tests/test_domain.py      # Domain layer
pytest tests/test_use_cases.py   # Use cases
pytest tests/test_api.py         # API integration tests
```

### Testing Types

- **Unit Tests:** Entities and domain logic
- **Integration Tests:** APIs and use cases
- **Contract Tests:** Repository interfaces
- **End-to-End Tests:** Complete user flows

## 🎯 DDD Principles

### Layer Separation

1. **Domain Layer:** 
   - Immutable entities with `@dataclass(frozen=True)`
   - Pure business logic
   - Repository interfaces

2. **Application Layer:**
   - Use case orchestration
   - Coordination between domain and infrastructure
   - Transactions and error handling

3. **Infrastructure Layer:**
   - Repository implementations
   - HTTP controllers (FastAPI)
   - External integrations

### Applied Principles

- **Dependency Inversion:** Higher layers depend on abstractions
- **Clean Architecture:** Dependency flow towards domain
- **Immutability:** Immutable entities for thread-safety
- **Repository Pattern:** Persistence abstraction
- **Use Cases:** Business logic orchestration

---

## 🚀 Getting Started Quick

1. **Fork this repository**
2. **Configure GitHub secrets:**
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY` 
   - `DOCKERHUB_USERNAME`
   - `DOCKERHUB_TOKEN`
3. **Push changes to `infra/`** → Deploy infrastructure
4. **Push changes to `app/`** → Deploy application
5. **Access application** via ALB endpoint

The project is designed to work out-of-the-box with minimal configuration! 