import {
    Duration, NestedStack, NestedStackProps, RemovalPolicy,
} from 'aws-cdk-lib';
import {Construct} from 'constructs';
import {AttributeType, Table} from 'aws-cdk-lib/aws-dynamodb';
import {Key} from 'aws-cdk-lib/aws-kms';
import {
    Effect, ManagedPolicy, PolicyStatement, Role, ServicePrincipal,
} from 'aws-cdk-lib/aws-iam';
import {PythonFunction} from '@aws-cdk/aws-lambda-python-alpha';
import {Runtime} from 'aws-cdk-lib/aws-lambda';
import {SqsEventSource} from 'aws-cdk-lib/aws-lambda-event-sources';
import {Queue} from 'aws-cdk-lib/aws-sqs';
import {Secret} from 'aws-cdk-lib/aws-secretsmanager';
import {CfnApp, CfnSMSChannel, CfnVoiceChannel} from 'aws-cdk-lib/aws-pinpoint';
import convertToSnakeCase from './utils/convert-to-snake-case';

interface Watchdog2ProcessingStackProps extends NestedStackProps {
    botName: string;
    receiverQueue: Queue;
    botSecretName: string;
}

export default class Watchdog2ProcessingStack extends NestedStack {
    contactInfoTable: Table;

    processingLambda: PythonFunction;

    constructor(scope: Construct, id: string, props: Watchdog2ProcessingStackProps) {
        super(scope, id, props);

        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        // Pinpoint set up

        const pinpointApp = new CfnApp(this, `PinpointApp${props.botName}`, {
            name: `PinpointApp${props.botName}`,
        });

        new CfnSMSChannel(this, `SMSChannel${props.botName}`, {
            applicationId: pinpointApp.ref,
            enabled: true,
        });

        new CfnVoiceChannel(this, `VoiceChannel${props.botName}`, {
            applicationId: pinpointApp.ref,
            enabled: true,
        });

        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        // DDB table to store contact info

        this.contactInfoTable = new Table(this, 'ContactInfoTable', {
            partitionKey: {
                name: 'discord_user',
                type: AttributeType.STRING,
            },
            tableName: 'contact_info',
            removalPolicy: RemovalPolicy.DESTROY,
            encryptionKey: new Key(this, 'ContactInfoTableKMSKey', {
                enableKeyRotation: true,
            }),
        });

        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        // Processing lambda

        const processingRole = new Role(this, `LambdaProcessingRole${props.botName}`, {
            assumedBy: new ServicePrincipal('lambda.amazonaws.com'),
            managedPolicies: [
                ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole'),
            ],
            roleName: `LambdaProcessingRole${props.botName}`,
        });

        processingRole.addToPolicy(new PolicyStatement({
            actions: [
                'mobiletargeting:SendMessages',
                'sms-voice:SendVoiceMessage',
            ],
            effect: Effect.ALLOW,
            resources: [
                `${pinpointApp.attrArn}/messages`,
                `arn:aws:sms-voice:${this.region}:${this.account}:/v1/sms-voice/voice/message`,
            ],
        }));

        // DDB permission for the function
        this.contactInfoTable.grantReadWriteData(processingRole);

        // Grant permissions to the secret, the
        // secret is not passed to the stack
        // directly to avoid circular dependencies.
        const botSecret = Secret.fromSecretPartialArn(this, 'BotSecret', `arn:aws:secretsmanager:${this.region}:${this.account}:secret:${props.botSecretName}`);
        botSecret.grantRead(processingRole);

        // The actual Lambda
        this.processingLambda = new PythonFunction(this, `LambdaProcessing${props.botName}`, {
            functionName: `LambdaProcessing${props.botName}`,
            runtime: Runtime.PYTHON_3_11,
            handler: convertToSnakeCase(props.botName),
            memorySize: 128,
            timeout: Duration.seconds(5),
            role: processingRole,
            environment: {
                BOT_SECRET_NAME: botSecret.secretName,
                SQS_QUEUE_URL: props.receiverQueue.queueUrl,
                CONTACT_INFO_TABLE_NAME: this.contactInfoTable.tableName,
                PINPOINT_APP_ID: pinpointApp.ref,
                ORIGINATION_NUMBER: '+18664799447',
            },
            entry: './src/',
            index: 'processing_lambdas/watchdog_2.py',
        });

        const eventSource = new SqsEventSource(props.receiverQueue);
        this.processingLambda.addEventSource(eventSource);

        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        // Commands update

        new PythonFunction(this, `CommandUpdates${props.botName}`, {
            functionName: `CommandUpdates${props.botName}`,
            runtime: Runtime.PYTHON_3_11,
            handler: `${convertToSnakeCase(props.botName)}_commands`,
            memorySize: 128,
            timeout: Duration.minutes(5),
            role: processingRole,
            environment: {
                BOT_SECRET_NAME: botSecret.secretName,
            },
            entry: './src/',
            index: 'command_updates/watchdog_2.py',
        });
    }
}
