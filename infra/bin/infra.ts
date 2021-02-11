#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import {EcrStack} from "../lib/ecr/ecr-stack";
import {StackUtil} from "../util/stack-util";

const app = new cdk.App();
new EcrStack(app, StackUtil.getStackName('REPOSITORY'));
