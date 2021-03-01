import * as cdk from "@aws-cdk/core";
import * as apiGateway from "@aws-cdk/aws-apigatewayv2";
import {HttpMethod} from "@aws-cdk/aws-apigatewayv2";
import * as ecr from "@aws-cdk/aws-ecr";
import * as lambda from "@aws-cdk/aws-lambda";
import {DockerImageCode} from "@aws-cdk/aws-lambda";
import {StackUtil} from "../../util/stack-util";
import {LambdaProxyIntegration} from "@aws-cdk/aws-apigatewayv2-integrations";
import secrets from "../../config/secrets";
import config from "config";

export class ApiGatewayStack extends cdk.Stack {
    constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        const repository = ecr.Repository.fromRepositoryAttributes(
            this,
            'StartExecutionFunctionRepository', {
                repositoryArn: `arn:aws:ecr:${cdk.Aws.REGION}:${cdk.Aws.ACCOUNT_ID}:repository/${StackUtil.getName('repo')}`,
                repositoryName: StackUtil.getName('repo'),
            }
        );

        const startExecutionFunction = new lambda.DockerImageFunction(this, 'StartExecutionFunction', {
            code: DockerImageCode.fromEcr(repository, {
                tag: 'start-execution',
            }),
            logRetention: 1,
            functionName: StackUtil.getUpperCaseName('START-EXECUTION'),
            environment: {
                STAGE: config.get('stage'),
                SLACK_SIGNING_SECRET: secrets.slackSigningSecret
            }
        });
        const startExecutionFunctionIntegration = new LambdaProxyIntegration({
            handler: startExecutionFunction,
        })

        const api = new apiGateway.HttpApi(this, 'HttpApi', {
            apiName: StackUtil.getUpperCaseName('HTTP-API'),
        });
        api.addRoutes({
            path: '/execute',
            methods: [HttpMethod.POST],
            integration: startExecutionFunctionIntegration,
        });
    }
}
