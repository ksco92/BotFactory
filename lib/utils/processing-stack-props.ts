import {
    NestedStackProps,
} from 'aws-cdk-lib';
import {
    Queue,
} from 'aws-cdk-lib/aws-sqs';


export default interface ProcessingStackProps extends NestedStackProps {
    botName: string;
    receiverQueue: Queue;
    botSecretName: string;
}