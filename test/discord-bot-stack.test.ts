/**
 * @file discord-bot-stack.test.ts
 * Tests for the DiscordBotStack in lib/discord-bot-stack.ts.
 */

import {
    App,
} from 'aws-cdk-lib';
import {
    Template,
} from 'aws-cdk-lib/assertions';
import DiscordBotStack from '../lib/discord-bot-stack';
import Watchdog2ProcessingStack from '../lib/watchdog2-processing-stack';

describe('DiscordBotStack', () => {
    /**
     * Test that the Discord Bot Stack creates expected resources.
     */
    it('should create the correct resources for a new DiscordBotStack', () => {
        const app = new App();
        const botName = 'Watchdog2';
        const zoneName = 'botfactory.lol';
        const hostedZoneId = 'abcdefg';

        const stack = new DiscordBotStack(app, 'DiscordBotStack', {
            env: {
                account: '8373873873',
                region: 'us-east-1',
            },
            botName,
            processingStackClass: Watchdog2ProcessingStack,
            hostedZoneId,
            zoneName,
        });

        const template = Template.fromStack(stack);

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
            Runtime: 'python3.13',
            FunctionName: `LambdaReceiver${botName}`,
            Handler: 'discord.discord_receiver.discord_receiver',
        });

        // Receiver queue
        template.hasResourceProperties('AWS::SQS::Queue', {
            QueueName: `SQS${botName}`,
        });

        // Two nested stacks: ProcessingStack + MonitoringStack
        template.resourceCountIs('AWS::CloudFormation::Stack', 2);

        // Certificate and Domain
        template.hasResourceProperties('AWS::CertificateManager::Certificate', {
            DomainName: zoneName,
        });

        // Additional checks for environment variables, secrets, etc.
        template.hasResourceProperties('AWS::SecretsManager::Secret', {
            Name: `bot/${botName}`,
        });
    });
});
