import * as cdk from "@aws-cdk/core";
import * as apiGateway from "@aws-cdk/aws-apigateway";
import * as ecr from "@aws-cdk/aws-ecr";
import * as lambda from "@aws-cdk/aws-lambda";
import {StackUtil} from "../../util/stack-util";
import {DockerImageCode} from "@aws-cdk/aws-lambda";

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
                tag: 'start-execution-function',
            }),
        });

        const restApi = new apiGateway.RestApi(this, 'RestApi', {
            deploy: false,
            restApiName: StackUtil.getName('api'),
            description: 'DeleteSlackFiles Rest API',
        });
        restApi.root.addResource('execute')
            .addMethod('POST', new apiGateway.LambdaIntegration(startExecutionFunction))
    }
}
