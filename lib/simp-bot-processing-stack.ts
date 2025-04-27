import {NestedStack, NestedStackProps, RemovalPolicy} from 'aws-cdk-lib';
import {Construct} from 'constructs';
import {AttributeType, Table} from 'aws-cdk-lib/aws-dynamodb';
import {Key} from 'aws-cdk-lib/aws-kms';
import {Queue} from 'aws-cdk-lib/aws-sqs';
import {PythonFunction} from '@aws-cdk/aws-lambda-python-alpha';
import createProcessingLambdaRole from './utils/create-processing-lambda-role';
import getBotSecret from './utils/get-bot-secret';
import createProcessingLambda from './utils/create-processing-lambda';
import createCommandUpdateLambda from './utils/create-command-update-lambda';

interface SimpBotProcessingStackProps extends NestedStackProps {
    botName: string;
    receiverQueue: Queue;
    botSecretName: string;
}

export default class SimpBotProcessingStack extends NestedStack {
    processingLambda: PythonFunction;

    constructor(scope: Construct, id: string, props: SimpBotProcessingStackProps) {
        super(scope, id, props);

        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        // DDB table to store points

        const pointsTable = new Table(this, 'PointsTable', {
            partitionKey: {
                name: 'transaction_id',
                type: AttributeType.STRING,
            },
            tableName: 'points',
            removalPolicy: RemovalPolicy.DESTROY,
            encryptionKey: new Key(this, 'PointsTableKMSKey', {
                enableKeyRotation: true,
                alias: 'PointsTableKMSKey',
                removalPolicy: RemovalPolicy.DESTROY,
            }),
        });

        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        // Processing lambda

        const processingRole = createProcessingLambdaRole(this, props.botName);
        const botSecret = getBotSecret(this, props.botSecretName);

        // Permissions
        botSecret.grantRead(processingRole);
        pointsTable.grantReadWriteData(processingRole);

        // The actual Lambda
        this.processingLambda = createProcessingLambda(
            this,
            props.botName,
            botSecret,
            processingRole,
            props.receiverQueue
        );

        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        // Command updates lambda

        createCommandUpdateLambda(this, props.botName, botSecret, processingRole);
    }
}
