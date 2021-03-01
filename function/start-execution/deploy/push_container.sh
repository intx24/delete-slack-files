#!/bin/bash
AWS_ACCOUNT=$(aws sts get-caller-identity --query 'Account' --output text)
docker tag local:start-execution $AWS_ACCOUNT.dkr.ecr.ap-northeast-1.amazonaws.com/delete-slack-files-repo:start-execution
docker push $AWS_ACCOUNT.dkr.ecr.ap-northeast-1.amazonaws.com/delete-slack-files-repo:start-execution