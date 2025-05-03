/**
 * @file create-command-update-lambda.test.ts
 * Tests for createCommandUpdateLambda in lib/utils/create-command-update-lambda.ts.
 */

import {
    App,
    Stack,
} from 'aws-cdk-lib';
import {
    Template,
} from 'aws-cdk-lib/assertions';
import {
    Role,
    ServicePrincipal,
    ManagedPolicy,
} from 'aws-cdk-lib/aws-iam';
import {
    Secret,
} from 'aws-cdk-lib/aws-secretsmanager';
import createCommandUpdateLambda from '../../lib/utils/create-command-update-lambda';

describe('createCommandUpdateLambda', () => {
    /**
     * Ensure that createCommandUpdateLambda sets up a Python function resource.
     */
    it('should create a PythonFunction for updating commands', () => {
        const app = new App();
        const stack = new Stack(app, 'TestStackCmdUpdate');

        // Minimal role
        const role = new Role(stack, 'TestRole', {
            assumedBy: new ServicePrincipal('lambda.amazonaws.com'),
            managedPolicies: [
                ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole'),
            ],
        });

        // Minimal secret
        const secret = new Secret(stack, 'TestSecret', {
            secretName: 'bot/SimpBot',
        });

        createCommandUpdateLambda(
            stack,
            'SimpBot',
            secret,
            role,
        );

        const template = Template.fromStack(stack);

        // Check for function
        template.hasResourceProperties('AWS::Lambda::Function', {
            FunctionName: 'CommandUpdatesSimpBot',
            Handler: 'command_updates.simp_bot.simp_bot_commands',
            Runtime: 'python3.11',
        });
    });
});
