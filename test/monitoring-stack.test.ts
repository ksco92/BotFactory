/**
 * @file monitoring-stack.test.ts
 * Tests for the MonitoringStack in lib/monitoring-stack.ts.
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
import {
    PythonFunction,
} from '@aws-cdk/aws-lambda-python-alpha';
import MonitoringStack from '../lib/monitoring-stack';
import {
    Runtime,
} from 'aws-cdk-lib/aws-lambda';

/**
 * Create a dummy PythonFunction for testing.
 * @param scope The test scope.
 * @param id The construct ID.
 * @returns A PythonFunction.
 */
function createDummyLambda(scope: Stack, id: string): PythonFunction {
    // Minimal placeholder for the test
    return new PythonFunction(scope, id, {
        entry: './src/',
        runtime: Runtime.PYTHON_3_13,
        handler: 'simp_bot',
        index: 'processing_lambdas/simp_bot.py',
    });
}

describe('MonitoringStack', () => {
    /**
     * It should synthesize without errors and create zero or more resources.
     * Currently, MonitoringStack does not add real AWS resources, but we confirm it deploys.
     */
    it('should synthesize a monitoring stack successfully', () => {
        const app = new App();
        const parentStack = new Stack(app, 'ParentStackForMonitoringTest');

        const queue = new Queue(parentStack, 'TestQueue');
        const lambdaReceiver = createDummyLambda(parentStack, 'DummyReceiverLambda');
        const lambdaProcessor = createDummyLambda(parentStack, 'DummyProcessorLambda');

        const monitoringStack = new MonitoringStack(parentStack, 'MonitoringStackTest', {
            botName: 'TestBot',
            receiverQueue: queue,
            processingFunction: lambdaProcessor,
            receiverFunction: lambdaReceiver,
        });

        const template = Template.fromStack(monitoringStack);
        // Currently the MonitoringStack has no CloudWatch alarms or dashboards,
        // so we just confirm that it does not fail to deploy.
        // If you add resources in the future, add hasResourceProperties checks here.

        // Confirm it is a nested stack or a stack with an actual template.
        // MonitoringStack extends NestedStack, so let's just ensure it synthesizes:
        expect(template.toJSON()).toBeDefined();
    });
});
