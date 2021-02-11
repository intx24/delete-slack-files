#!/bin/bash

SECRET_FILE="./secrets.json"

if [ ! -e $SECRET_FILE ]; then
  echo "Secret file does not exist."
  exit 1
fi

JSON=$(cat $SECRET_FILE)
SLACK_API_TOKEN=$(echo "$JSON" | jq -r ".slackApiToken")

aws ssm put-parameter \
    --name "/delete-slack-files/slack-api-token" \
    --value "$SLACK_API_TOKEN" \
    --type "SecureString" \
    --overwrite