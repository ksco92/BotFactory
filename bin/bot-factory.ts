#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import {
    NestedStack,
} from 'aws-cdk-lib';
import DiscordBotStack from '../lib/discord-bot-stack';
import Watchdog2ProcessingStack from '../lib/watchdog2-processing-stack';
import SimpBotProcessingStack from '../lib/simp-bot-processing-stack';

const hostedZoneId = 'Z007921225FIW4IMG71RE';
const zoneName = 'botfactory.lol';

const app = new cdk.App();

const bots: {
    botName: string,
    processingStackClass: typeof NestedStack,
}[] = [
    {
        botName: 'Watchdog2',
        processingStackClass: Watchdog2ProcessingStack,
    },
    {
        botName: 'SimpBot',
        processingStackClass: SimpBotProcessingStack,
    },
];

bots.forEach(bot => {
    new DiscordBotStack(app, `${bot.botName}Stack`, {
        botName: bot.botName,
        processingStackClass: bot.processingStackClass,
        hostedZoneId,
        zoneName,
    });
});
