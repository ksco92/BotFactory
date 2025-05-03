import typescriptEslint from '@typescript-eslint/eslint-plugin';
import tsParser from '@typescript-eslint/parser';
import path from 'node:path';
import {
    fileURLToPath,
} from 'node:url';
import js from '@eslint/js';
import {
    FlatCompat,
} from '@eslint/eslintrc';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const compat = new FlatCompat({
    baseDirectory: __dirname,
    recommendedConfig: js.configs.recommended,
    allConfig: js.configs.all,
});

export default [
    // Extend recommended configs
    ...compat.extends('eslint:recommended', 'plugin:@typescript-eslint/recommended'),
    {
        // Lint your lib code
        files: [
            'lib/**/*.{ts,tsx}',
            'bin/**/*.{ts,tsx}',
            'test/**/*.{ts,tsx}',
        ],
        ignores: [
            'lib/**/*.{js,d.ts}',
            'bin/**/*.{js,d.ts}',
        ],
    },
    {
        plugins: {
            '@typescript-eslint': typescriptEslint,
        },
        languageOptions: {
            parser: tsParser,
            ecmaVersion: 'latest',
            sourceType: 'module',
            parserOptions: {
                ecmaFeatures: {
                    jsx: true,
                },
            },
        },
        rules: {
            // Require trailing commas in multiline arrays/objects
            'comma-dangle': [
                'error',
                {
                    arrays: 'always-multiline',
                    objects: 'always-multiline',
                    imports: 'always-multiline',
                    exports: 'always-multiline',
                    functions: 'ignore',
                },
            ],

            // Force arrays to be multiline if they have at least one element
            // and put each element on its own line
            'array-bracket-newline': [
                'error',
                {
                    multiline: true,
                    minItems: 1,
                },
            ],
            'array-element-newline': [
                'error',
                {
                    multiline: true,
                    minItems: 1,
                },
            ],

            // Force object literals to be multiline if they have properties
            'object-curly-newline': [
                'error',
                {
                    ObjectExpression: {
                        multiline: true,
                        minProperties: 1,
                    },
                    ObjectPattern: {
                        multiline: true,
                        minProperties: 1,
                    },
                    ImportDeclaration: {
                        multiline: true,
                        minProperties: 1,
                    },
                    ExportDeclaration: {
                        multiline: true,
                        minProperties: 1,
                    },
                },
            ],

            // Require single quotes (with optional template literals)
            quotes: [
                'error',
                'single',
                {
                    avoidEscape: true,
                    allowTemplateLiterals: true,
                },
            ],

            // Quote object keys only when necessary
            'quote-props': [
                'error',
                'as-needed',
            ],

            // Put each key/value pair on its own line
            'object-property-newline': [
                'error',
                {
                    allowAllPropertiesOnSameLine: false,
                },
            ],

            // NEW RULE: enforce 4-space indentation
            indent: [
                'error',
                4,
            ],

            '@typescript-eslint/no-unused-vars': [
                'error',
                {
                    argsIgnorePattern: '^_',
                    varsIgnorePattern: '^_',
                },
            ],
        },
    },
];