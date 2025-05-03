import {
    Construct,
} from 'constructs';
import {
    ManagedPolicy, PolicyStatement, Role, ServicePrincipal,
} from 'aws-cdk-lib/aws-iam';
import {
    Stack,
} from 'aws-cdk-lib';

export default function createProcessingLambdaRole(scope: Construct, botName: string) {
    const processingRole = new Role(scope, `LambdaProcessingRole${botName}`, {
        assumedBy: new ServicePrincipal('lambda.amazonaws.com'),
        managedPolicies: [
            ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole'),
        ],
        roleName: `LambdaProcessingRole${botName}`,
    });

    processingRole.addToPolicy(new PolicyStatement({
        actions: [
            'kms:Decrypt',
        ],
        resources: [
            `arn:aws:kms:${Stack.of(scope).region}:${Stack.of(scope).account}:key/*`,
        ],
    }));

    return processingRole;
}
