module.exports = {
	env: {
		browser: true,
		es2021: true,
	},
	parser: '@typescript-eslint/parser',
	parserOptions: {
		ecmaVersion: 'latest',
		sourceType: 'module',
		project: './tsconfig.json',
	},
	plugins: ['@typescript-eslint', 'prettier'],
	extends: [
		'eslint:recommended',
		'plugin:@typescript-eslint/recommended',
		'plugin:prettier/recommended',
	],
	rules: {
		'@typescript-eslint/explicit-member-accessibility': [
			'error',
			{
				accessibility: 'explicit',
				overrides: {
					constructors: 'no-public',
				},
			},
		],
		'@typescript-eslint/consistent-type-exports': 'warn',
		'@typescript-eslint/consistent-type-imports': [
			'warn',
			{
				fixStyle: 'inline-type-imports',
			},
		],
		'@typescript-eslint/explicit-function-return-type': 'warn',
		'@typescript-eslint/explicit-module-boundary-types': 'warn',
		'@typescript-eslint/naming-convention': [
			'error',
			{
				selector: 'interface',
				format: ['PascalCase'],
				custom: {
					regex: '[A-Z]',
					match: true,
				},
			},
		],
		'@typescript-eslint/no-explicit-any': 'warn',
		'@typescript-eslint/no-unused-vars': [
			'warn',
			{
				argsIgnorePattern: '^_',
				destructuredArrayIgnorePattern: '^_',
				caughtErrorsIgnorePattern: '^ignore',
			},
		],
		'@typescript-eslint/no-var-requires': 'error',
		'no-mixed-spaces-and-tabs': 'warn',
		'no-restricted-imports': [
			'error',
			{
				patterns: [
					{
						group: ['*/features/*/*'],
						message: 'Please import from the index file instead',
					},
					{
						group: ['**.scss', '!./*.scss'],
						message: 'Styles should be defined in the same folder as the component',
					},
				],
			},
		],
		'prettier/prettier': [
			'warn',
			{
				endOfLine: 'auto',
			},
		],
		semi: ['warn', 'always'],
	},
	ignorePatterns: ['/*', '!./src', '!./utils'],
};
