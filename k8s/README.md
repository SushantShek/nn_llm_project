# Kubernetes Deployment Setup Guide

This guide outlines the Kubernetes resources and what needs to be configured for the person-finder application.

## Prerequisites

- EKS Cluster running in AWS
- kubectl configured to access your EKS cluster
- AWS ECR repository for the application image
- OpenAI API key

## GitHub Secrets Required

Add the following secrets to your GitHub repository:

1. **AWS_ROLE_ARN** - IAM role ARN for OIDC trust with GitHub Actions
2. **AWS_REGION** - AWS region (e.g., `eu-north-1`)
3. **ECR_REPOSITORY** - ECR repository name (e.g., `person-finder`)
4. **EKS_CLUSTER_NAME** - EKS cluster name (e.g., `person-finder-cluster`)
5. **OPENAI_API_KEY** - Your OpenAI API key (required for the application to run)

## Kubernetes Resources

### 1. Namespace (namespace.yaml)
- Creates the `person-finder` namespace for all application resources

### 2. ServiceAccount (serviceaccount.yaml)
- Creates a ServiceAccount for the deployment
- Sets up RBAC permissions to read ConfigMaps and Secrets

### 3. ConfigMap (configmap.yaml)
- Stores application configuration (e.g., LOG_LEVEL)
- Can be updated without redeploying the application

### 4. Secrets (secret.yaml)
- **openai-secret**: Stores the OpenAI API key (created dynamically from GitHub secrets)
- **ecr-secret**: Placeholder for ECR authentication (automatically included)

**Note**: The OpenAI API key is created from the `OPENAI_API_KEY` GitHub secret during deployment. The placeholder value in `secret.yaml` is only used if the secret is not provided.

### 5. Deployment (deployment.yaml)
- Creates 2 replicas of the person-finder application
- Pull policy: Always (ensures fresh image on each update)
- Resource requests:
  - CPU: 250m
  - Memory: 256Mi
- Resource limits:
  - CPU: 500m
  - Memory: 512Mi
- Health probes:
  - Liveness probe: Checks `/health` endpoint every 10 seconds (30s initial delay)
  - Readiness probe: Checks `/health` endpoint every 5 seconds (10s initial delay)

### 6. Service (service.yaml)
- Type: LoadBalancer (exposes the application externally)
- Port mapping: 80 (external) → 8000 (container)

## Application Requirements

The application must implement the following:

1. **Health Check Endpoint** (`/health`)
   - Should return HTTP 200 when the application is healthy
   - Used by Kubernetes liveness and readiness probes
   - Example endpoint:
     ```python
     @app.get("/health")
     async def health_check():
         return {"status": "healthy"}
     ```

2. **Environment Variables**
   - `OPENAI_API_KEY`: Your OpenAI API key (provided via Kubernetes secret)
   - `LOG_LEVEL`: Logging level from ConfigMap (default: INFO)

## Deployment Process

When you push to the `main` branch:

1. GitHub Actions workflow triggers
2. Builds and pushes Docker image to ECR
3. Updates kubeconfig to access EKS cluster
4. Applies Kubernetes resources:
   - Namespace
   - ServiceAccount & RBAC
   - OpenAI secret (from `OPENAI_API_KEY` GitHub secret)
   - ConfigMap
   - Service
   - Deployment with the new image
5. Waits for 5 minutes for the deployment to become ready
6. Reports success or failure with pod details/logs

## Troubleshooting

If the deployment fails with timeout or pod crashes:

### Check Pod Status
```bash
kubectl get pods -n person-finder
kubectl describe pod <pod-name> -n person-finder
```

### Check Pod Logs
```bash
kubectl logs -n person-finder -l app=person-finder --tail=100
```

### Common Issues

1. **ImagePullBackOff**
   - ECR credentials issue
   - Check AWS credentials and IAM permissions

2. **CrashLoopBackOff**
   - Application failing to start
   - Check logs for missing environment variables
   - Verify OpenAI API key is valid

3. **Pending**
   - Insufficient resources in the cluster
   - Check node capacity: `kubectl top nodes`

4. **Health Check Failing**
   - Ensure the `/health` endpoint is implemented
   - Check if the application is listening on port 8000
   - Verify the application is accepting HTTP requests

## Update Configuration

### Update Log Level
```bash
kubectl set env configmap/person-finder-config LOG_LEVEL=DEBUG -n person-finder
```

### Update OpenAI API Key
```bash
kubectl create secret generic openai-secret \
  --from-literal=API_KEY='your-new-key' \
  -n person-finder --dry-run=client -o yaml | kubectl apply -f -

# Force deployment to pick up new secret
kubectl rollout restart deployment/person-finder -n person-finder
```

### Scale Replicas
```bash
kubectl scale deployment person-finder --replicas=3 -n person-finder
```

## Monitoring

Check deployment status:
```bash
kubectl rollout status deployment/person-finder -n person-finder
```

Get deployment events:
```bash
kubectl describe deployment person-finder -n person-finder
```

View service details:
```bash
kubectl get svc person-finder -n person-finder
```
