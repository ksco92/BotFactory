/**
 * @file watchdog2-processing-stack.test.ts
 * Tests for Watchdog2ProcessingStack in lib/watchdog2-processing-stack.ts.
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
import Watchdog2ProcessingStack from '../lib/watchdog2-processing-stack';
import ProcessingStackProps from '../lib/utils/processing-stack-props';

describe('Watchdog2ProcessingStack', () => {
    /**
     * Validate that the stack sets up the required resources.
     */
    it('should create the contact info table, KMS key, Pinpoint, and processing Lambda', () => {
        const app = new App();
        const parentStack = new Stack(app, 'ParentWatchdog2Test');

        const queue = new Queue(parentStack, 'Watchdog2Queue', {
            queueName: 'SQSWatchdog2Test',
        });

        const props: ProcessingStackProps = {
            botName: 'Watchdog2',
            receiverQueue: queue,
            botSecretName: 'bot/Watchdog2',
        };

        const wd2Stack = new Watchdog2ProcessingStack(parentStack, 'WD2Stack', props);
        const template = Template.fromStack(wd2Stack);

        // Check the DDB contact info table
        template.hasResourceProperties('AWS::DynamoDB::Table', {
            TableName: 'contact_info',
        });

        // Check KMS Key for the table
        template.hasResourceProperties('AWS::KMS::Key', {
            EnableKeyRotation: true,
        });

        // Check for Pinpoint resources
        template.hasResourceProperties('AWS::Pinpoint::App', {
            Name: 'PinpointAppWatchdog2',
        });

        // Check for the processing Lambda
        template.hasResourceProperties('AWS::Lambda::Function', {
            FunctionName: 'LambdaProcessingWatchdog2',
            Handler: 'processing_lambdas.watchdog_2.watchdog2',
        });

        // Check for command updates Lambda
        template.hasResourceProperties('AWS::Lambda::Function', {
            FunctionName: 'CommandUpdatesWatchdog2',
        });
    });
});
