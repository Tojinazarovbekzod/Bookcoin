# BookCoin – AWS ECS Deployment Guide

## Architecture

```
Internet → Route 53 (domain) → ALB (HTTPS/443) → ECS Fargate (Django) → RDS MySQL
                                        ↕
                                   ACM (SSL cert)
```

## One-time Setup Steps

### 1. Prerequisites
- AWS CLI installed and configured (`aws configure`)
- Docker installed
- Domain name (buy one in AWS Route 53 or transfer from another registrar)

---

### 2. Create VPC & Networking
```bash
# Use default VPC, or create a new one via the AWS Console:
# VPC → Create VPC → with subnets (at least 2 public, 2 private in different AZs)
```

---

### 3. Create RDS MySQL (Database)
```bash
aws rds create-db-instance \
  --db-instance-identifier bookcoin-db \
  --db-instance-class db.t3.micro \
  --engine mysql \
  --engine-version 8.0 \
  --master-username bookcoin_admin \
  --master-user-password "YOUR_STRONG_PASSWORD" \
  --db-name bookcoin \
  --allocated-storage 20 \
  --storage-type gp2 \
  --no-publicly-accessible \
  --region us-east-1
```
> Note the RDS endpoint from the output (takes ~5 min to create).

---

### 4. Store Secrets in AWS Secrets Manager
```bash
REGION="us-east-1"
ACCOUNT=$(aws sts get-caller-identity --query Account --output text)

# Generate a strong secret key first:
python -c "import secrets; print(secrets.token_urlsafe(50))"

aws secretsmanager create-secret --name bookcoin/SECRET_KEY    --secret-string "YOUR_GENERATED_SECRET_KEY" --region $REGION
aws secretsmanager create-secret --name bookcoin/DB_HOST       --secret-string "your-rds-endpoint.rds.amazonaws.com" --region $REGION
aws secretsmanager create-secret --name bookcoin/DB_USER       --secret-string "bookcoin_admin" --region $REGION
aws secretsmanager create-secret --name bookcoin/DB_PASSWORD   --secret-string "YOUR_STRONG_PASSWORD" --region $REGION
aws secretsmanager create-secret --name bookcoin/ALLOWED_HOSTS --secret-string "yourdomain.com,www.yourdomain.com" --region $REGION
aws secretsmanager create-secret --name bookcoin/EMAIL_HOST_USER     --secret-string "your@gmail.com" --region $REGION
aws secretsmanager create-secret --name bookcoin/EMAIL_HOST_PASSWORD --secret-string "your-gmail-app-password" --region $REGION
```

---

### 5. Create IAM Roles for ECS
```bash
# ecsTaskExecutionRole – lets ECS pull images and read secrets
aws iam create-role --role-name ecsTaskExecutionRole \
  --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"ecs-tasks.amazonaws.com"},"Action":"sts:AssumeRole"}]}'

aws iam attach-role-policy --role-name ecsTaskExecutionRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy

# Allow reading Secrets Manager
aws iam attach-role-policy --role-name ecsTaskExecutionRole \
  --policy-arn arn:aws:iam::aws:policy/SecretsManagerReadWrite
```

---

### 6. Create ECS Cluster
```bash
aws ecs create-cluster --cluster-name bookcoin-cluster --region us-east-1
```

---

### 7. Create CloudWatch Log Group
```bash
aws logs create-log-group --log-group-name /ecs/bookcoin --region us-east-1
```

---

### 8. Build & Push First Docker Image
```bash
# Update aws/ecs-task-definition.json first:
# Replace ACCOUNT_ID and REGION with your actual values

chmod +x aws/deploy.sh
./aws/deploy.sh
```

---

### 9. Create Application Load Balancer (ALB)
In AWS Console:
1. EC2 → Load Balancers → Create Load Balancer → Application
2. Name: `bookcoin-alb`
3. Scheme: Internet-facing
4. Listeners: HTTP 80 (add HTTPS 443 after step 10)
5. Availability Zones: select at least 2
6. Create Target Group: type=IP, port=8000, health check path=`/admin/`

---

### 10. Get SSL Certificate via ACM
```bash
aws acm request-certificate \
  --domain-name "yourdomain.com" \
  --subject-alternative-names "www.yourdomain.com" \
  --validation-method DNS \
  --region us-east-1
```
Then validate via Route 53 (click "Create DNS records" in ACM console).

---

### 11. Create ECS Service
In AWS Console:
1. ECS → Clusters → bookcoin-cluster → Create Service
2. Launch type: FARGATE
3. Task definition: bookcoin (latest revision)
4. Service name: bookcoin-service
5. Desired tasks: 1 (increase later)
6. VPC: your VPC, private subnets
7. Load balancer: bookcoin-alb → target group you created
8. Auto-scaling: optional (set min=1, max=3, CPU 70% target)

---

### 12. Register Domain & Configure DNS (Route 53)

**Option A – Buy domain directly in Route 53:**
1. Route 53 → Registered Domains → Register Domain
2. Search for your domain (e.g. `bookcoin.uz`)
3. Follow the purchase flow (~$12-15/year for .com)

**Option B – Transfer existing domain:**
1. Get auth code from your current registrar
2. Route 53 → Registered Domains → Transfer Domain

**Configure DNS after domain is ready:**
```bash
# Get your ALB DNS name:
aws elbv2 describe-load-balancers --query 'LoadBalancers[?LoadBalancerName==`bookcoin-alb`].DNSName' --output text

# In Route 53 → Hosted Zones → yourdomain.com:
# Create A record (alias) → point to bookcoin-alb
# Create A record for www → same ALB
```

---

### 13. Add HTTPS Listener to ALB
In AWS Console:
1. EC2 → Load Balancers → bookcoin-alb → Listeners → Add listener
2. Protocol: HTTPS, Port: 443
3. SSL certificate: select your ACM certificate
4. Default action: Forward to bookcoin target group
5. Add redirect rule: HTTP → HTTPS (port 80 → 443)

---

### 14. Run Django Migrations on First Deploy
```bash
# Get the ECS cluster task ARN after the service starts:
aws ecs list-tasks --cluster bookcoin-cluster --service-name bookcoin-service

# Run migrations via ECS exec (one-time):
aws ecs execute-command \
  --cluster bookcoin-cluster \
  --task TASK_ARN \
  --container bookcoin \
  --command "python manage.py migrate" \
  --interactive
```

---

## Deploying Updates

Every time you push a code change:
```bash
./aws/deploy.sh
```

This builds a new image, pushes it to ECR, and triggers a rolling update in ECS with zero downtime.

---

## Estimated Monthly Cost

| Service          | Spec             | Cost/month |
|------------------|------------------|------------|
| ECS Fargate      | 0.5 vCPU / 1 GB  | ~$15       |
| RDS MySQL        | db.t3.micro 20GB | ~$15       |
| ALB              | 1 LCU            | ~$18       |
| Route 53 (DNS)   | 1 hosted zone    | ~$0.50     |
| ECR storage      | < 1 GB           | ~$0.10     |
| **Total**        |                  | **~$49/mo**|

> Domain registration: ~$12-15/year for .com
