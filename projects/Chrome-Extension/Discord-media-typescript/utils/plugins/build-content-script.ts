import colorLog from '../log';
import { build, PluginOption } from 'vite';
import { resolve } from 'path';

const CWD = process.cwd();

const packages = [
	{
		content: resolve(CWD, 'src/pages/content/index.ts'),
	},
];

const outDir = resolve(CWD, 'dist');

export default function buildContentScript(): PluginOption {
	return {
		name: 'build-content',
		async buildEnd() {
			console.log('buildEnd');
			for (const _package of packages) {
				console.log('buildEnd', _package);
				await build({
					publicDir: false,
					plugins: [],
					build: {
						outDir,
						sourcemap: process.env.__DEV__ === 'true',
						emptyOutDir: false,
						rollupOptions: {
							input: _package,
							output: {
								entryFileNames: (chunk) => {
									return `src/pages/${chunk.name}/index.js`;
								},
							},
						},
					},
					configFile: false,
				});
			}
			colorLog('Content code build sucessfully', 'success');
		},
	};
}