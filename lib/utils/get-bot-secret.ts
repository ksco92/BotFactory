import {Secret} from 'aws-cdk-lib/aws-secretsmanager';
import {Construct} from 'constructs';
import {Stack} from 'aws-cdk-lib';

export default function getBotSecret(scope: Construct, botSecretName: string) {
    // Grant permissions to the secret, the
    // secret is not passed to the stack
    // directly to avoid circular dependencies.
    return Secret.fromSecretPartialArn(scope, 'BotSecret', `arn:aws:secretsmanager:${Stack.of(scope).region}:${Stack.of(scope).account}:secret:${botSecretName}`);
}
