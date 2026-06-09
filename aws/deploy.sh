#!/bin/bash
# BookCoin – AWS ECS Fargate deployment script
# Usage: ./aws/deploy.sh
# Prerequisites: AWS CLI configured, Docker installed

set -euo pipefail

# ── Configuration – change these ─────────────────────────────────────────────
AWS_REGION="us-east-1"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REPO="bookcoin"
ECS_CLUSTER="bookcoin-cluster"
ECS_SERVICE="bookcoin-service"
IMAGE_TAG=$(git rev-parse --short HEAD)
ECR_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}"

echo "==> Deploying BookCoin to AWS ECS"
echo "    Region:  ${AWS_REGION}"
echo "    Account: ${AWS_ACCOUNT_ID}"
echo "    Tag:     ${IMAGE_TAG}"

# ── Step 1: Authenticate Docker with ECR ─────────────────────────────────────
echo ""
echo "==> [1/5] Authenticating Docker with ECR..."
aws ecr get-login-password --region "${AWS_REGION}" \
  | docker login --username AWS --password-stdin "${ECR_URI}"

# ── Step 2: Create ECR repository (skips if exists) ──────────────────────────
echo "==> [2/5] Ensuring ECR repository exists..."
aws ecr describe-repositories --repository-names "${ECR_REPO}" --region "${AWS_REGION}" 2>/dev/null \
  || aws ecr create-repository --repository-name "${ECR_REPO}" --region "${AWS_REGION}"

# ── Step 3: Build & push Docker image ────────────────────────────────────────
echo "==> [3/5] Building Docker image..."
docker build -t "${ECR_REPO}:${IMAGE_TAG}" .
docker tag "${ECR_REPO}:${IMAGE_TAG}" "${ECR_URI}:${IMAGE_TAG}"
docker tag "${ECR_REPO}:${IMAGE_TAG}" "${ECR_URI}:latest"

echo "==> Pushing image to ECR..."
docker push "${ECR_URI}:${IMAGE_TAG}"
docker push "${ECR_URI}:latest"

# ── Step 4: Update task definition with new image ─────────────────────────────
echo "==> [4/5] Updating ECS task definition..."
sed "s|ACCOUNT_ID|${AWS_ACCOUNT_ID}|g; s|REGION|${AWS_REGION}|g" \
    aws/ecs-task-definition.json > /tmp/task-def.json

NEW_TASK_DEF=$(aws ecs register-task-definition \
  --cli-input-json file:///tmp/task-def.json \
  --region "${AWS_REGION}" \
  --query 'taskDefinition.taskDefinitionArn' \
  --output text)

echo "    New task definition: ${NEW_TASK_DEF}"

# ── Step 5: Force new deployment ──────────────────────────────────────────────
echo "==> [5/5] Deploying to ECS service..."
aws ecs update-service \
  --cluster "${ECS_CLUSTER}" \
  --service "${ECS_SERVICE}" \
  --task-definition "${NEW_TASK_DEF}" \
  --force-new-deployment \
  --region "${AWS_REGION}"

echo ""
echo "==> Deployment triggered. Monitor at:"
echo "    https://${AWS_REGION}.console.aws.amazon.com/ecs/home?region=${AWS_REGION}#/clusters/${ECS_CLUSTER}/services/${ECS_SERVICE}/events"
