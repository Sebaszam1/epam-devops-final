# DevOps Final Project: FastAPI on AWS EKS

## 🎯 What This Project Does

This project showcases a production-ready FastAPI application deployed on AWS using Kubernetes (EKS), with fully automated CI/CD pipelines. I've built everything from scratch following industry best practices:

- **Modern Python API** built with FastAPI and Domain-Driven Design
- **Cloud Infrastructure** managed with Terraform on AWS
- **Container Orchestration** using Kubernetes (EKS)
- **Automated Deployments** via GitHub Actions
- **Production-Ready** health checks

## 🏗️ Architecture Overview

### High-Level System Design

```
┌─────────────────────────────────────────────────────────────────┐
│                          GitHub Repository                      │
├─────────────────────────────────────────────────────────────────┤
│  App Changes                    │  Infrastructure Changes       │
│      ↓                          │           ↓                   │
├─────────────────────────────────────────────────────────────────┤
│                     GitHub Actions (CI/CD)                      │
│  ┌─────────────────────────────┐  │  ┌─────────────────────────┐│
│  │        App Pipeline         │  │  │     Infra Pipeline      ││
│  │ • Test                      │  │  │ • Terraform             ││
│  │ • Build                     │  │  │ • Plan & Apply          ││
│  │ • Deploy                    │  │  │ • AWS Resources         ││
│  └─────────────────────────────┘  │  └─────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│                        AWS Cloud (us-east-1)                    │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    VPC (10.0.0.0/16)                        ││
│  │  ┌─────────────────┐        ┌─────────────────────────────┐ ││
│  │  │ Public Subnets  │        │      Private Subnets        │ ││
│  │  │ • ALB           │   ←→   │ • EKS Worker Nodes          │ ││
│  │  │ • NAT Gateway   │        │ • FastAPI Pods (2 replicas) │ ││
│  │  │ • Internet GW   │        │ • Internal Services         │ ││
│  │  └─────────────────┘        └─────────────────────────────┘ ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### Application Architecture (Domain-Driven Design)

I've structured my FastAPI application using DDD principles for maintainability and testability:

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                      │
├─────────────────────────────────────────────────────────────┤
│  🌐 Infrastructure Layer (controllers.py)                   │
│     • REST API endpoints (/health, /api/v1/*)               │
│     • HTTP request/response handling                        │
│     • External interface (web controllers)                  │
├─────────────────────────────────────────────────────────────┤
│  ⚙️  Application Layer (use_cases.py)                       │
│     • Business logic orchestration                          │
│     • Use case implementations                              │
│     • Service coordination                                  │
├─────────────────────────────────────────────────────────────┤
│  🏛️  Domain Layer (entities.py, repositories.py)            │
│     • Core business entities                                │
│     • Domain rules and validation                           │
│     • Repository interfaces (contracts)                     │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Setup Instructions

### Prerequisites

**Required Accounts:**
- AWS account with administrative permissions
- DockerHub account (for container registry)
- GitHub repository with Actions enabled

**AWS IAM User Requirements:**
Your AWS user needs the following permissions:
- EC2 Full Access (for VPC, subnets, security groups)
- EKS Full Access (for Kubernetes cluster)
- IAM Full Access (for roles and policies)
- ElasticLoadBalancing Full Access (for ALB)

### Step 1: Fork and Configure Repository

1. **Fork this repository** to your GitHub account

2. **Clone your forked repository:**
```bash
git clone https://github.com/Sebaszam1/epam-devops-final.git
cd epam-devops-final
```

### Step 2: Configure GitHub Secrets

Add these **required secrets**:

```
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key_here
DOCKERHUB_USERNAME=your_dockerhub_username
DOCKERHUB_TOKEN=your_dockerhub_access_token
```

### Step 3: Automated Cloud Deployment

Once you've configured the secrets deployment is fully automated:

**🏗️ Deploy Infrastructure First:**
```bash
# Make any change to infra/ directory (or create empty commit)
git commit --allow-empty -m "Deploy infrastructure"
git push origin main
```

**⏱️ Wait for Infrastructure (10-15 minutes):**
- Monitor progress in GitHub Actions tab
- Infrastructure pipeline will create VPC, EKS cluster, and ALB
- Check AWS Console to see resources being created

**🚀 Deploy Application:**
```bash
# Make any change to app/ directory (or create empty commit)
git commit --allow-empty -m "Deploy application"
git push origin main
```

**🎉 Access Your Application:**
- Get ALB URL from GitHub Actions logs
- Or run: `kubectl get ingress` (after configuring kubectl locally)
- Your app will be available at: `http://your-alb-url.amazonaws.com`


## 🔄 CI/CD Pipelines Description

I've implemented two main pipelines that work together to provide a complete deployment automation:

### Infrastructure Pipeline (`infra.yml`)

**Purpose:** Manages all AWS infrastructure using Terraform

**When it runs:**
- Any changes pushed to the `infra/` directory
- Changes to the pipeline file itself

**What it does:**

1. **🔍 Validation Phase:**
   - Checks Terraform syntax
   - Validates configuration files
   - Ensures proper formatting

2. **📋 Planning Phase:**
   - Generates execution plan
   - Shows what resources will be created/modified
   - Estimates costs and changes

3. **🚀 Deployment Phase:**
   - Creates VPC with public/private subnets
   - Sets up EKS cluster (Kubernetes v1.29)
   - Configures worker nodes (t3.small instances)
   - Creates IAM roles and security groups
   - Sets up Application Load Balancer

**Resources Created:**
- **VPC:** 10.0.0.0/16 with 2 availability zones
- **EKS Cluster:** Managed Kubernetes with 1-2 worker nodes
- **Load Balancer:** Internet-facing ALB for external access
- **Security:** IAM roles, security groups, and policies

### Application Pipeline (`app.yml`)

**Purpose:** Builds, tests, and deploys the FastAPI application

**When it runs:**
- Any changes pushed to the `app/` directory
- Manual trigger for redeployments

**What it does:**

1. **🧪 Testing Phase:**
   - Sets up Python 3.11 environment
   - Installs all dependencies
   - Runs comprehensive test suite
   - Generates coverage reports

2. **🐳 Build Phase:**
   - Creates optimized Docker image
   - Uses multi-stage build for smaller size
   - Scans for security vulnerabilities
   - Pushes to DockerHub registry

3. **☸️ Infrastructure Setup:**
   - Configures AWS credentials
   - Updates kubectl configuration
   - Verifies EKS cluster connectivity

4. **⚖️ Load Balancer Setup:**
   - Installs Helm package manager
   - Deploys AWS Load Balancer Controller
   - Configures IAM service accounts
   - Waits for controller readiness

5. **🚀 Application Deployment:**
   - Applies configuration (ConfigMap)
   - Deploys application (2 replicas)
   - Creates internal service
   - Configures external ingress
   - Performs rolling update
   - Validates health checks

### Pipeline Flow Example

Here's what happens when you make a change:

```
Developer pushes code
         ↓
GitHub detects changes
         ↓
    ┌─────────────────┐         ┌─────────────────┐
    │ Infrastructure  │   OR    │  Application    │
    │    Pipeline     │         │    Pipeline     │
    │                 │         │                 │
    │ 1. Validate     │         │ 1. Test         │
    │ 2. Plan         │         │ 2. Build        │
    │ 3. Apply        │         │ 3. Deploy       │
    └─────────────────┘         └─────────────────┘
         ↓                               ↓
    AWS Infrastructure              Kubernetes App
    (VPC, EKS, ALB)                (Pods, Services)
         ↓                               ↓
         └───────────────┬───────────────┘
                         ↓
              🎉 Live Application 🎉
    http://your-alb-url.amazonaws.com
```

## 📁 Project Structure

Our project is organized for clarity and maintainability:

```
devops-final-project/
│
├── 🐍 app/                        # Python FastAPI Application
│   ├── main.py                   # Application entry point
│   ├── Dockerfile                # Multi-stage container build
│   ├── requirements.txt          # Python dependencies
│   │
│   ├── domain/                   # 🏛️ Domain Layer (Business Logic)
│   │   ├── entities.py          # Core business entities
│   │   └── repositories.py      # Repository interfaces
│   │
│   ├── application/              # ⚙️ Application Layer (Use Cases)
│   │   └── use_cases.py         # Business logic orchestration
│   │
│   └── infrastructure/           # 🌐 Infrastructure Layer (External)
│       ├── controllers.py       # FastAPI REST endpoints
│       └── repositories.py      # Repository implementations
│
├── 🏗️ infra/                      # Infrastructure as Code (Terraform)
│   ├── main.tf                  # Main AWS resources (VPC, EKS)
│   ├── variables.tf             # Input variables and configuration
│   ├── outputs.tf               # Exported values (URLs, IDs)
│   ├── versions.tf              # Provider version constraints
│   ├── backend.tf               # Remote state configuration
│   ├── terraform.tfvars         # Variable values
│   └── iam-policy.json          # IAM policy definitions
│
├── ☸️ k8s/                        # Kubernetes Manifests
│   ├── deployment.yaml          # Application deployment (2 replicas)
│   ├── service.yaml             # Internal service (ClusterIP)
│   ├── ingress.yaml             # External access (ALB)
│   └── configmap.yaml           # Configuration variables
│
├── 🔄 .github/workflows/          # CI/CD Pipeline Definitions
│   ├── app.yml                  # Application build & deploy pipeline
│   └── infra.yml                # Infrastructure deployment pipeline
│
├── 🧪 tests/                      # Test Suite
│   ├── test_domain.py           # Domain layer tests
│   ├── test_use_cases.py        # Application layer tests
│   └── test_repositories.py     # Infrastructure layer tests
│
├── 📋 requirements.txt            # Testing and development dependencies
├── 📋 pytest.ini                 # Test configuration
└── 📖 README.md                  # This documentation
```

## 🌐 API Endpoints

Once deployed, your application provides these endpoints:

| Method | Endpoint | Description | Example Response |
|--------|----------|-------------|------------------|
| `GET` | `/` | Welcome message | `{"message": "Welcome to FastAPI!"}` |
| `GET` | `/health` | Detailed health check | `{"status": "healthy", "timestamp": "...", "version": "1.0.0"}` |
| `GET` | `/api/v1/health` | Simple health check | `{"status": "OK"}` |
| `GET` | `/api/v1/user/{username}` | User information | `{"username": "john", "message": "Hello john!"}` |

### Usage Examples

```bash
# Get application URL (after deployment)
kubectl get ingress

# Test endpoints
curl http://your-alb-url.amazonaws.com/health
curl http://your-alb-url.amazonaws.com/api/v1/user/sebas

# Interactive API documentation
open http://your-alb-url.amazonaws.com/docs
```
