import {App} from 'aws-cdk-lib';
import {Template} from 'aws-cdk-lib/assertions';
import DiscordBotStack from '../lib/discord-bot-stack';

test('Test resources in Discord Bot Stack stack', () => {
    const app = new App();
    const botName = 'Watchdog2';
    const zoneName = 'botfactory.lol';

    const stack = new DiscordBotStack(app, 'DiscordBotStack', {
        env: {
            account: '8373873873',
            region: 'us-east-1',
        },
        botName,
        processingStackClassName: 'Watchdog2ProcessingStack',
        processingStackClassFile: './watchdog2-processing-stack.ts',
        hostedZoneId: 'someinvalidzoneid',
        zoneName,
    });

    const template = Template.fromStack(stack);

    /// ////////////////////////////////////////////
    /// ////////////////////////////////////////////
    /// ////////////////////////////////////////////
    /// ////////////////////////////////////////////
    // Receiver Lambda

    template.hasResourceProperties('AWS::IAM::Role', {
        AssumeRolePolicyDocument: {
            Statement: [
                {
                    Action: 'sts:AssumeRole',
                    Effect: 'Allow',
                    Principal: {
                        Service: 'lambda.amazonaws.com',
                    },
                },
            ],
        },
        RoleName: `LambdaReceiverRole${botName}`,
    });

    template.hasResourceProperties('AWS::Lambda::Function', {
        Runtime: 'python3.11',
        FunctionName: `LambdaReceiver${botName}`,
        Handler: 'discord.discord_receiver',
    });

    /// ////////////////////////////////////////////
    /// ////////////////////////////////////////////
    /// ////////////////////////////////////////////
    /// ////////////////////////////////////////////
    // Receiver queue

    template.hasResourceProperties('AWS::SQS::Queue', {
        QueueName: `SQS${botName}`,
    });

    /// ////////////////////////////////////////////
    /// ////////////////////////////////////////////
    /// ////////////////////////////////////////////
    /// ////////////////////////////////////////////
    // Processing Stack

    template.resourceCountIs('AWS::CloudFormation::Stack', 1);

    /// ////////////////////////////////////////////
    /// ////////////////////////////////////////////
    /// ////////////////////////////////////////////
    /// ////////////////////////////////////////////
    // API Gateway

    template.hasResourceProperties('AWS::CertificateManager::Certificate', {
        DomainName: `${botName}.${zoneName}`,
    });

    // TODO: specific APIG tests
});
