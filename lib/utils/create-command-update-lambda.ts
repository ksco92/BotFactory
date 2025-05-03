import {
    PythonFunction,
} from '@aws-cdk/aws-lambda-python-alpha';
import {
    Runtime,
} from 'aws-cdk-lib/aws-lambda';
import {
    Duration,
} from 'aws-cdk-lib';
import {
    Role,
} from 'aws-cdk-lib/aws-iam';
import {
    Construct,
} from 'constructs';
import {
    ISecret,
} from 'aws-cdk-lib/aws-secretsmanager';
import convertToSnakeCase from './convert-to-snake-case';

export default function createCommandUpdateLambda(
    scope: Construct,
    botName: string,
    botSecret: ISecret,
    processingRole: Role
) {
    new PythonFunction(scope, `CommandUpdates${botName}`, {
        functionName: `CommandUpdates${botName}`,
        runtime: Runtime.PYTHON_3_11,
        handler: `${convertToSnakeCase(botName)}_commands`,
        memorySize: 128,
        timeout: Duration.minutes(5),
        role: processingRole,
        environment: {
            BOT_SECRET_NAME: botSecret.secretName,
        },
        entry: './src/',
        index: `command_updates/${convertToSnakeCase(botName)}.py`,
    });
}
