import { PAGE_URL } from '~/utils';

import { BackgroundScriptMessage, PopUpScriptMessage } from '~/utils/messages';

const BODY = document.body.getElementsByTagName('ul').item(0);
const FULL_PAGE_BUTTON = document.getElementById('fullPage');
const CLEAR_BUTTON = document.getElementById('clear');
const REMOVE_LAST = document.getElementById('removeLast');
if (!BODY || !FULL_PAGE_BUTTON || !CLEAR_BUTTON || !REMOVE_LAST) {
	throw alert('Error: popupScript.ts');
}

//to list
// TODO: Add a real type for list (no any)
let list: any | undefined;

function sendAction(action: string | string[]): void {
	return chrome.runtime.sendMessage<PopUpScriptMessage>({ action: action }, function(response) {
		console.log('response', response);
		if (action === 'list') {
			list = response;
			console.log(list, typeof list);
			for (let i = 0; i < list.length; i++) {
				addPageMedia(list[i]);
			}
		}
		return response;
	});
}

function removeElement(element: HTMLElement): void {
	const elementList = document.getElementsByTagName('a');
	const link = elementList.item(0);
	if (!link) return;
	const url = link.href;
	sendAction(['removeElement', url]);
	element.remove();
}

function addPageMedia(url: string): void {
	// send url to background script
	console.log('addPageMedia', url);
	
	const date = new Date();
	
	const newDiv = document.createElement('li');
	newDiv.classList.add('element');
	
	const a = document.createElement('a');
	a.href = url;
	const title = getTitle(url);
	if (title) a.textContent = title;
	newDiv.appendChild(a);
	
	if (url.includes('mp4') || url.includes('webm')) {
		const video = document.createElement('video');
		video.classList.add('video');
		video.src = url;
		video.controls = true;
		newDiv.appendChild(video);
	} else {
		const image = document.createElement('img');
		image.classList.add('image');
		image.src = url;
		newDiv.appendChild(image);
	}
	
	const span = document.createElement('span');
	span.classList.add('timestamp');
	span.textContent = date.toLocaleString();
	newDiv.appendChild(span);
	
	const downDiv = document.createElement('div');
	downDiv.classList.add('downContainer');
	
	const download = document.createElement('a');
	download.classList.add('download-button');
	download.href = url;
	download.textContent = 'Télécharger';
	
	const delButton = document.createElement('button');
	delButton.textContent = '🗑️';
	delButton.id = 'removeButton';
	delButton.addEventListener('click', () => {
		removeElement(newDiv);
	});
	
	downDiv.appendChild(download);
	downDiv.appendChild(delButton);
	newDiv.appendChild(downDiv);
	
	BODY?.appendChild(newDiv);
}

sendAction('list');

chrome.runtime.onMessage.addListener((message: BackgroundScriptMessage, _sender, sendResponse) => {
	if (message.addNewUrl) {
		addPageMedia(message.addNewUrl);
		sendResponse('added');
		console.log('added');
	}
});

function getTitle(url: string): string | undefined {
	const split = url.split('/');
	return split[split.length - 1];
}

function clear(): void {
	list = [];
	sendAction('clear');
	const elementList = document.getElementsByTagName('element');
	const element = elementList.item(0);
	if (element) element.innerHTML = '';
}

function removeLastElement(): void {
	if (!list) return;
	sendAction('removeLast');
	list.pop();
	const elementList = document.getElementsByTagName('ul');
	const element = elementList.item(0);
	if (!element) return;
	const size = element.getElementsByTagName('li').length;
	if (size < 1) return;
	element.getElementsByTagName('li')[size - 1]?.remove();
}

FULL_PAGE_BUTTON.addEventListener('click', (): void => {
	//open the page of popup
	chrome.tabs.create({ url: PAGE_URL });
});

CLEAR_BUTTON.addEventListener('click', (): void => {
	console.log('clear');
	clear();
});

REMOVE_LAST.addEventListener('click', (): void => {
	console.log('removeLast');
	removeLastElement();
});
