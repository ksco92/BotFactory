/**
 * @file create-processing-lambda-role.test.ts
 * Tests for createProcessingLambdaRole in lib/utils/create-processing-lambda-role.ts.
 */

import {
    App,
    Stack,
} from 'aws-cdk-lib';
import {
    Template,
} from 'aws-cdk-lib/assertions';
import createProcessingLambdaRole from '../../lib/utils/create-processing-lambda-role';

describe('createProcessingLambdaRole', () => {
    /**
     * Test that the role is created with the correct name and policies.
     */
    it('should create a role with KMS Decrypt permissions and correct name', () => {
        const app = new App();
        const stack = new Stack(app, 'TestStackRole');

        createProcessingLambdaRole(stack, 'MyBot');

        const template = Template.fromStack(stack);

        template.hasResourceProperties('AWS::IAM::Role', {
            RoleName: 'LambdaProcessingRoleMyBot',
        });

        // Check that we have a policy allowing KMS:Decrypt
        template.hasResourceProperties('AWS::IAM::Policy', {
            PolicyDocument: {
                Statement: [
                    {
                        Action: 'kms:Decrypt',
                        Effect: 'Allow',
                    },
                ],
            },
        });
    });
});
