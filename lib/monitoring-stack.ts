import {
    NestedStack, NestedStackProps,
} from 'aws-cdk-lib';
import {
    Construct,
} from 'constructs';
import {
    PythonFunction,
} from '@aws-cdk/aws-lambda-python-alpha';
import {
    Queue,
} from 'aws-cdk-lib/aws-sqs';

interface MonitoringStackProps extends NestedStackProps {
    botName: string;
    receiverQueue: Queue;
    processingFunction: PythonFunction;
    receiverFunction: PythonFunction;
}

export default class MonitoringStack extends NestedStack {
    constructor(scope: Construct, id: string, props: MonitoringStackProps) {
        super(scope, id, props);

        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        /// ////////////////////////////////////////////
        // stuff

        // TODO: monitoring of lambda receiver
        // TODO: monitoring of lambda processing
        // TODO: monitoring of SQS

        console.log(props.botName);
    }
}
