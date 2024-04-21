module.exports = {
    testEnvironment: 'node',
    roots: [
        '<rootDir>/test',
    ],
    testMatch: [
        '**/*.test.ts',
    ],
    transform: {
        '^.+\\.(tsx|ts)?$': 'ts-jest',
    },
    globals: {
        'ts-jest': {
            tsConfig: 'tsconfig.json',
        },
    },
    preset: 'ts-jest',
};
