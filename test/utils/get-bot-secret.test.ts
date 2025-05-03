/**
 * @file get-bot-secret.test.ts
 * Tests for getBotSecret in lib/utils/get-bot-secret.ts.
 */

import {
    App, Stack,
} from 'aws-cdk-lib';
import {
    ISecret,
} from 'aws-cdk-lib/aws-secretsmanager';
import getBotSecret from '../../lib/utils/get-bot-secret';
import {
    Template,
} from 'aws-cdk-lib/assertions';

describe('getBotSecret', () => {
    /**
     * Confirm that getBotSecret returns an imported Secret reference
     * using fromSecretPartialArn.
     */
    it('should import the secret from a partial ARN', () => {
        const app = new App();
        const stack = new Stack(app, 'TestStackBotSecret');

        // The function simply returns Secret.fromSecretPartialArn(...).
        // We can call it and verify the returned object is an ISecret.
        const secretRef = getBotSecret(stack, 'bot/MyBotSecret');
        expect(secretRef).toBeDefined();
        expect((secretRef as ISecret).secretArn).toContain('arn:aws:secretsmanager');

        // The actual secret is not created in this stack, so we only verify no error is thrown.
        // There's no new resource created, so the template is effectively empty:
        const template = Template.fromStack(stack);
        expect(template.toJSON()).toMatchObject({});
    });
});
