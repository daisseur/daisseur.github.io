import { PAGE_URL } from '~/utils';
import { ContentScriptMessage } from '~/utils/messages';

const OVERED_URLS: string[] = [];
const IMAGES_EXT = ['png', 'jpg', 'jpeg', 'gif', 'webp'];
const VIDEO_EXT = ['mp4', 'webm'];

function addMedia(url: string): void {
	// send url to background script and show response
	chrome.runtime.sendMessage<ContentScriptMessage>({ NewUrl: url }, function(response) {
		console.log(`response of ${url}:`, response);
	});
}

function checkMediaUrl(url: string): string | null {
	if (!url && url.includes('discord')) return null; // TODO: Fix this
	let base = url;
	const splitted_url = url.split('?');
	if (splitted_url.length > 1 && splitted_url[0]) {
		base = splitted_url[0];
	}
	let ext = base.split('.').pop();
	if (!ext) return null;
	ext = ext.toLowerCase();
	if (IMAGES_EXT.includes(ext) || VIDEO_EXT.includes(ext)) {
		return base;
	} else {
		return null;
	}
}

function handleMouseHover(event: MouseEvent): void {
	console.log('handleMouseHover', event.target);
	const element = event.target as HTMLElement; // TODO: Fix this
	if (!element) return;
	let select_url: string | null;
	const src = element.getAttribute('src');
	if (PAGE_URL.includes('discord')) {
		if (src) {
			select_url = src;
		} else {
			select_url = element.getAttribute('href');
		}
	} else {
		select_url = src;
	}
	if (!select_url) return;
	
	const check = checkMediaUrl(select_url);
	if (select_url !== OVERED_URLS[OVERED_URLS.length - 1] && check) {
		OVERED_URLS.push(check);
	}
	
	if (OVERED_URLS.length > 10) {
		OVERED_URLS.shift();
	}
	for (let i = 0; i < OVERED_URLS.length; i++) {
		if (OVERED_URLS[i] === undefined) {
			// remove element
			OVERED_URLS.splice(i, 1);
		}
	}
}

document.addEventListener('mouseover', handleMouseHover, { passive: true });
document.addEventListener('keydown', function(event) {
	if (event.key === 'a') {
		console.log('pressed a, sending', OVERED_URLS);
		const url = OVERED_URLS[OVERED_URLS.length - 1];
		url && addMedia(url);
	}
});
