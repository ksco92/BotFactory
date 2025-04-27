#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import DiscordBotStack from '../lib/discord-bot-stack';

const hostedZoneId = 'Z007921225FIW4IMG71RE';
const zoneName = 'botfactory.lol';

const app = new cdk.App();

new DiscordBotStack(app, 'Watchdog2Stack', {
    botName: 'Watchdog2',
    processingStackClassName: 'Watchdog2ProcessingStack',
    processingStackClassFile: './watchdog2-processing-stack.ts',
    hostedZoneId,
    zoneName,
});

new DiscordBotStack(app, 'SimpBotStack', {
    botName: 'SimpBot',
    processingStackClassName: 'SimpBotProcessingStack',
    processingStackClassFile: './simp-bot-processing-stack.ts',
    hostedZoneId,
    zoneName,
});
