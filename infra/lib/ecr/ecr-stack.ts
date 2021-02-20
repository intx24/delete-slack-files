import * as cdk from '@aws-cdk/core';
import * as ecr from '@aws-cdk/aws-ecr';
import {TagStatus} from '@aws-cdk/aws-ecr';
import {StackUtil} from "../../util/stack-util";

export class EcrStack extends cdk.Stack {
    constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        new ecr.Repository(this, 'Repository', {
            repositoryName: StackUtil.getName('repo'),
            lifecycleRules: [
                {
                    tagStatus: TagStatus.ANY,
                    maxImageCount: 1,
                    description: 'leave only one image.'
                }
            ],
            imageScanOnPush: false,
        });
    }
}
