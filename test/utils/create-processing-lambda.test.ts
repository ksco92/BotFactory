/**
 * @file create-processing-lambda.test.ts
 * Tests for createProcessingLambda in lib/utils/create-processing-lambda.ts.
 */

import {
    App,
    Stack,
} from 'aws-cdk-lib';
import {
    Template,
    Match,
} from 'aws-cdk-lib/assertions';
import {
    Role,
    ServicePrincipal,
    ManagedPolicy,
} from 'aws-cdk-lib/aws-iam';
import {
    Secret,
} from 'aws-cdk-lib/aws-secretsmanager';
import {
    Queue,
} from 'aws-cdk-lib/aws-sqs';
import createProcessingLambda from '../../lib/utils/create-processing-lambda';

describe('createProcessingLambda', () => {
    /**
     * Test that the function is created with an SQS event source, environment, etc.
     */
    it('should create a Python function with an SQS event source', () => {
        const app = new App();
        const stack = new Stack(app, 'TestStackProcessingLambda');

        const role = new Role(stack, 'TestProcessingRole', {
            assumedBy: new ServicePrincipal('lambda.amazonaws.com'),
            managedPolicies: [
                ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole'),
            ],
        });

        const secret = new Secret(stack, 'TestSecret', {
            secretName: 'bot/SimpBot',
        });

        const queue = new Queue(stack, 'TestQueue', {
            queueName: 'MyQueue',
        });

        createProcessingLambda(
            stack,
            'SimpBot',
            secret,
            role,
            queue,
        );

        const template = Template.fromStack(stack);

        template.hasResourceProperties('AWS::Lambda::Function', {
            FunctionName: 'LambdaProcessingSimpBot',
            Runtime: 'python3.13',
            Environment: {
                Variables: {
                    BOT_SECRET_NAME: Match.anyValue(),
                    SQS_QUEUE_URL: Match.anyValue(),
                },
            },
        });

        // Check for event source mapping to SQS
        template.resourceCountIs('AWS::Lambda::EventSourceMapping', 1);
    });
});
