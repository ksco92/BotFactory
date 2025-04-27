import {PythonFunction} from '@aws-cdk/aws-lambda-python-alpha';
import {Runtime} from 'aws-cdk-lib/aws-lambda';
import {Duration} from 'aws-cdk-lib';
import {Construct} from 'constructs';
import {ISecret} from 'aws-cdk-lib/aws-secretsmanager';
import {Role} from 'aws-cdk-lib/aws-iam';
import {Queue} from 'aws-cdk-lib/aws-sqs';
import {SqsEventSource} from 'aws-cdk-lib/aws-lambda-event-sources';
import convertToSnakeCase from './convert-to-snake-case';

export default function createProcessingLambda(
    scope: Construct,
    botName: string,
    botSecret: ISecret,
    processingRole: Role,
    receiverQueue: Queue
) {
    const processingLambda = new PythonFunction(scope, `LambdaProcessing${botName}`, {
        functionName: `LambdaProcessing${botName}`,
        runtime: Runtime.PYTHON_3_11,
        handler: convertToSnakeCase(botName),
        memorySize: 128,
        timeout: Duration.seconds(5),
        role: processingRole,
        environment: {
            BOT_SECRET_NAME: botSecret.secretName,
            SQS_QUEUE_URL: receiverQueue.queueUrl,
        },
        entry: './src/',
        index: `processing_lambdas/${convertToSnakeCase(botName)}.py`,
    });

    const eventSource = new SqsEventSource(receiverQueue);
    processingLambda.addEventSource(eventSource);

    return processingLambda;
}
