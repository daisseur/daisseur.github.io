import type { Manifest } from 'webextension-polyfill';
import pkg from '../package.json';

const manifest: Manifest.WebExtensionManifest = {
	// TODO Manifest update to v3
	manifest_version: 2,
	name: pkg.name,
	version: pkg.version,
	description: pkg.description,
	icons: {
		128: 'discord_neon_logo.png',
	},
	permissions: ['activeTab', 'contextMenus', 'downloads', 'tabs', 'runtime'],
	background: {
		scripts: ['src/pages/background/index.js'],
		persistent: false,
	},
	content_scripts: [
		{
			matches: ['<all_urls>'],
			js: ['src/pages/content/index.js'],
		},
	],
	browser_action: {
		default_title: pkg.name,
		default_popup: 'src/pages/popup/index.html',
	},
};

export default manifest;
