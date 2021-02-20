#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import {EcrStack} from "../lib/ecr/ecr-stack";
import {StackUtil} from "../util/stack-util";
import {ApiGatewayStack} from "../lib/api-gateway/api-gateway-stack";

const app = new cdk.App();

// const apiGatewayStack = new ApiGatewayStack(app, StackUtil.getStackName('APIGATEWAY'));

new EcrStack(app, StackUtil.getStackName('REPOSITORY'))
    // .addDependency(apiGatewayStack);
