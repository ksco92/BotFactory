import {
    Duration, RemovalPolicy, Stack, StackProps, Tags,
} from 'aws-cdk-lib';
import {Construct} from 'constructs';
import {Runtime} from 'aws-cdk-lib/aws-lambda';
import {
    ManagedPolicy, PolicyStatement, Role, ServicePrincipal,
} from 'aws-cdk-lib/aws-iam';
import {Key} from 'aws-cdk-lib/aws-kms';
import {Queue} from 'aws-cdk-lib/aws-sqs';
import importSync from 'import-sync';
import {
    Deployment, LambdaIntegration, LambdaRestApi, Model, PassthroughBehavior,
} from 'aws-cdk-lib/aws-apigateway';
import {ARecord, HostedZone, RecordTarget} from 'aws-cdk-lib/aws-route53';
import {ApiGatewayDomain} from 'aws-cdk-lib/aws-route53-targets';
import * as fs from 'fs';
import {Certificate, CertificateValidation} from 'aws-cdk-lib/aws-certificatemanager';
import {Secret} from 'aws-cdk-lib/aws-secretsmanager';
import {PythonFunction} from '@aws-cdk/aws-lambda-python-alpha';
import MonitoringStack from './monitoring-stack';

interface DiscordBotStackProps extends StackProps {
    botName: string;
    processingStackClassName: string;
    processingStackClassFile: string;
    hostedZoneId: string;
    zoneName: string;
}

export default class DiscordBotStack extends Stack {
    readonly botName: string;

    readonly queue: Queue;

    readonly botSecret: Secret;

    constructor(scope: Construct, id: string, props: DiscordBotStackProps) {
        super(scope, id, props);

        this.botName = props.botName;

        Tags.of(this).add('Bot', this.botName);

        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        // Secret

        this.botSecret = new Secret(this, `BotSecret${this.botName}`, {
            secretName: `bot/${this.botName}`,
            encryptionKey: new Key(this, `BotSecret${this.botName}KMSKey`, {
                enableKeyRotation: true,
                alias: `BotSecret${this.botName}KMSKey`,
                removalPolicy: RemovalPolicy.DESTROY,
            }),
        });

        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        // Receiver queue

        this.queue = new Queue(this, `SQS${this.botName}`, {
            encryptionMasterKey: new Key(this, `SQS${this.botName}KMSKey`, {
                enableKeyRotation: true,
                alias: `SQS${this.botName}`,
                removalPolicy: RemovalPolicy.DESTROY,
            }),
            queueName: `SQS${this.botName}`,
            visibilityTimeout: Duration.seconds(60),
        });

        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        // Receiver Lambda

        const receiverRole = new Role(this, `LambdaReceiverRole${this.botName}`, {
            assumedBy: new ServicePrincipal('lambda.amazonaws.com'),
            managedPolicies: [
                ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole'),
            ],
            roleName: `LambdaReceiverRole${this.botName}`,
        });

        receiverRole.addToPolicy(new PolicyStatement({
            actions: [
                'kms:Decrypt',
            ],
            resources: [
                '*',
            ],
        }));

        this.queue.grantSendMessages(receiverRole);
        this.botSecret.grantRead(receiverRole);

        const lambdaReceiver = new PythonFunction(this, `LambdaReceiver${props.botName}`, {
            functionName: `LambdaReceiver${props.botName}`,
            runtime: Runtime.PYTHON_3_11,
            handler: 'discord_receiver',
            memorySize: 128,
            timeout: Duration.seconds(5),
            role: receiverRole,
            environment: {
                BOT_SECRET_NAME: this.botSecret.secretName,
                SQS_QUEUE_URL: this.queue.queueUrl,
            },
            entry: './src/',
            index: 'discord/discord_receiver.py',
        });

        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        // Processing stack

        const plug = importSync(props.processingStackClassFile);
        const constructorName = Object.keys(plug)[0];

        // @ts-ignore
        const processingStack = new plug[constructorName](this, `ProcessingStack${this.botName}`, {
            botName: this.botName,
            receiverQueue: this.queue,
            botSecretName: `bot/${this.botName}`,
        });

        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        // API Gateway

        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        // DNS

        const publicHostedZone = HostedZone.fromHostedZoneAttributes(this, `PublicHostedZone${this.botName}`, {
            hostedZoneId: props.hostedZoneId,
            zoneName: props.zoneName,
        });

        const certificate = new Certificate(this, `Certificate${this.botName}`, {
            domainName: publicHostedZone.zoneName,
            validation: CertificateValidation.fromDns(publicHostedZone),
            subjectAlternativeNames: [
                `*.${publicHostedZone.zoneName}`,
            ],
            certificateName: `Certificate${this.botName}`,
        });

        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        // API

        const api = new LambdaRestApi(this, `API${this.botName}`, {
            proxy: false,
            handler: lambdaReceiver,
            deploy: true,
            deployOptions: {
                stageName: 'prod',
            },
            domainName: {
                domainName: `${this.botName.toLowerCase()}.${publicHostedZone.zoneName}`,
                certificate,
            },
        });

        new ARecord(this, `APIARecord${this.botName}`, {
            recordName: `${this.botName.toLowerCase()}.${publicHostedZone.zoneName}`,
            zone: publicHostedZone,
            target: RecordTarget.fromAlias(new ApiGatewayDomain(api.domainName!)),
        });

        const requestTemplate = fs.readFileSync('./lib/utils/apig-mapping-template.txt', 'utf8');

        const resource = api.root.addResource(this.botName);

        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        // API Responses

        const integration = new LambdaIntegration(lambdaReceiver, {
            proxy: true,
            integrationResponses: [
                {
                    statusCode: '401',
                    selectionPattern: '.*[UNAUTHORIZED].*',
                },
                {
                    statusCode: '500',
                    selectionPattern: '.*[ERROR].*',
                },
                {
                    statusCode: '500',
                    selectionPattern: '.*[BAD_REQUEST].*',
                },
                {
                    statusCode: '200',
                },
            ],
            passthroughBehavior: PassthroughBehavior.WHEN_NO_MATCH,
            requestTemplates: {
                'application/json': requestTemplate,
            },
        });

        const postMethod = resource.addMethod('POST', integration);

        postMethod.addMethodResponse({
            statusCode: '401',
            responseModels: {
                'application/json': Model.EMPTY_MODEL,
            },
        });

        postMethod.addMethodResponse({
            statusCode: '500',
            responseModels: {
                'application/json': Model.EMPTY_MODEL,
            },
        });

        postMethod.addMethodResponse({
            statusCode: '400',
            responseModels: {
                'application/json': Model.EMPTY_MODEL,
            },
        });

        postMethod.addMethodResponse({
            statusCode: '200',
            responseModels: {
                'application/json': Model.EMPTY_MODEL,
            },
        });

        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        // API Deployment

        new Deployment(this, `APIDeployment${this.botName}`, {
            api,
        });

        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        // Monitoring stack

        new MonitoringStack(this, `MonitoringStack${this.botName}`, {
            botName: this.botName,
            receiverQueue: this.queue,
            processingFunction: processingStack.processingLambda,
            receiverFunction: lambdaReceiver,
        });

        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        // Command updates

        // TODO: Add Lambda that runs the command updates on deployment.
    }
}
