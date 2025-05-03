/**
 * @file simp-bot-processing-stack.test.ts
 * Tests for the SimpBotProcessingStack in lib/simp-bot-processing-stack.ts.
 */

import {
    App,
    Stack,
} from 'aws-cdk-lib';
import {
    Template,
} from 'aws-cdk-lib/assertions';
import {
    Queue,
} from 'aws-cdk-lib/aws-sqs';
import SimpBotProcessingStack from '../lib/simp-bot-processing-stack';
import {
    NestedStack,
} from 'aws-cdk-lib';
import ProcessingStackProps from '../lib/utils/processing-stack-props';

describe('SimpBotProcessingStack', () => {
    /**
     * Test the creation of the resources inside the SimpBotProcessingStack.
     */
    it('should create DDB table, KMS key, Lambda, and command update Lambda', () => {
        const app = new App();
        const parentStack = new Stack(app, 'ParentStackForSimpBotTest');

        // Minimal props for the nested stack
        const queue = new Queue(parentStack, 'TestQueue', {
            queueName: 'TestQueueSimpBot',
        });

        const props: ProcessingStackProps = {
            botName: 'SimpBot',
            receiverQueue: queue,
            botSecretName: 'bot/SimpBot',
        };

        const simpBotStack = new SimpBotProcessingStack(parentStack, 'SimpBotStack', props);

        // Because it's a nested stack, get the template from the nested stack itself
        const template = Template.fromStack(simpBotStack as unknown as NestedStack);

        // Check for DDB table with tableName = 'points'
        template.hasResourceProperties('AWS::DynamoDB::Table', {
            TableName: 'points',
        });

        // Check for KMS Key for the table
        template.hasResourceProperties('AWS::KMS::Key', {
            // We don't have an Alias check in CloudFormation, but we can do a partial check:
            EnableKeyRotation: true,
        });

        // Check for the processing Lambda
        template.hasResourceProperties('AWS::Lambda::Function', {
            FunctionName: 'LambdaProcessingSimpBot',
        });

        // Check for the command update Lambda
        template.hasResourceProperties('AWS::Lambda::Function', {
            FunctionName: 'CommandUpdatesSimpBot',
        });
    });
});
