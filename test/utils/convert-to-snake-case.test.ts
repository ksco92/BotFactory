/**
 * @file convert-to-snake-case.test.ts
 * Tests for convertToSnakeCase function in lib/utils/convert-to-snake-case.ts.
 */

import convertToSnakeCase from '../../lib/utils/convert-to-snake-case';

describe('convertToSnakeCase', () => {
    /**
     * Test converting a typical string with spaces.
     */
    it('should convert strings with spaces to snake case', () => {
        const input = 'Hello World Example';
        const output = convertToSnakeCase(input);
        expect(output).toBe('hello_world_example');
    });

    /**
     * Test converting a PascalCase string.
     */
    it('should convert PascalCase strings to snake case', () => {
        const input = 'HelloWorldExample';
        const output = convertToSnakeCase(input);
        expect(output).toBe('hello_world_example');
    });

    /**
     * Test converting an already snake-cased string.
     */
    it('should handle an already snake-cased string gracefully', () => {
        const input = 'hello_world_example';
        const output = convertToSnakeCase(input);
        expect(output).toBe('hello_world_example');
    });
});
