# Cloud Native DevSecOps Platform

DevSecOps project built around a small FastAPI application. The application itself is intentionally simple: the main goal is to work on the infrastructure, deployment, scaling, security and troubleshooting around it.

So far, the project includes a tested FastAPI REST API with health and readiness endpoints, structured logging and environment-based configuration.

The application is packaged as a multi-stage Docker image and runs as a non-root user. Locally, it is deployed to a Kubernetes cluster created with kind.

The Kubernetes deployment currently includes:

* a Deployment managing the application replicas
* a ClusterIP Service for internal networking and service discovery
* liveness and readiness probes
* configuration through ConfigMaps
* CPU and memory requests and limits
* Horizontal Pod Autoscaling based on CPU metrics
* metrics-server for resource metrics
* Ingress for external HTTP access

The Kubernetes manifests have also been converted into a Helm chart, with separate values for staging and production environments.

## Roadmap

The next stage is focused on CI/CD and cloud infrastructure.

Planned work includes:

* GitHub Actions for CI
* Semgrep for SAST
* Trivy for dependency and container scanning
* Amazon ECR for container images
* AWS networking and Amazon EKS
* Terraform for infrastructure as code
* OIDC authentication between GitHub Actions and AWS
* staging and production deployments
* OWASP ZAP for DAST
* Prometheus, Grafana and CloudWatch
* Kubernetes RBAC and security hardening
* resilience testing and incident postmortems

## Final Goal

The final goal is to build a workflow where a code change goes through testing and security checks, produces a container image, is deployed first to staging and later promoted to production.