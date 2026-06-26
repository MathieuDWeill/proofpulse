# Deployment guide

## Local Docker

```bash
docker compose up --build
curl http://localhost:8080/health
curl -X POST http://localhost:8080/demo/seed | jq
```

## Minimal cloud deployment

1. Build Docker image.
2. Push to ECR.
3. Run on ECS Fargate behind an Application Load Balancer.
4. Add S3 bucket for evidence bundles.
5. Add DynamoDB tables for targets/incidents.
6. Add EventBridge scheduled rules for probe workers.
7. Add Bedrock integration when AWS credentials are available.

## Demo deployment shortcut

For hackathon speed, deploy the API to any container host first, then keep the AWS architecture in the pitch. The important part is that the product roadmap maps naturally to AWS credits.
