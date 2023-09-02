import { resolve } from 'path';
import { defineConfig } from 'vite';

const root = resolve(__dirname, 'src');
const pagesDir = resolve(root, 'pages');
const assetsDir = resolve(root, 'assets');
const outDir = resolve(__dirname, 'dist');
const publicDir = resolve(__dirname, 'public');

export default defineConfig({
	resolve: {
		alias: {
			'~': root,
			'~assets': assetsDir,
			'~pages': pagesDir,
		},
	},
	// plugins: [makeManifest(), buildContentScript()],
	publicDir,
	build: {
		outDir,
		sourcemap: process.env.__DEV__ === 'true',
		emptyOutDir: true,
		rollupOptions: {
			input: {
				// devtools: resolve(pagesDir, 'devtools', 'index.html'),
				// panel: resolve(pagesDir, 'panel', 'index.html'),
				background: resolve(pagesDir, 'background', 'index.ts'),
				content: resolve(pagesDir, 'content', 'index.ts'),
				popup: resolve(pagesDir, 'popup', 'index.html'),
				// newtab: resolve(pagesDir, 'newtab', 'index.html'),
				// options: resolve(pagesDir, 'options', 'index.html'),
			},
			output: {
				entryFileNames: (chunk) => `src/pages/${chunk.name}/index.js`,
			},
		},
	},
});