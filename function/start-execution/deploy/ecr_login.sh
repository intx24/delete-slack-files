#!/bin/bash
AWS_ACCOUNT=$(aws sts get-caller-identity --query 'Account' --output text)
aws ecr get-login-password | docker login --username AWS --password-stdin $AWS_ACCOUNT.dkr.ecr.ap-northeast-1.amazonaws.com