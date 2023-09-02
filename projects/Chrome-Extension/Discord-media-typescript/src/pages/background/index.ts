import {
	BackgroundScriptMessage,
	ContentScriptMessage,
	PopUpScriptMessage,
} from '~/utils/messages';

let INTERN_LIST: string[] = [];

function backgroundLog(...args: unknown[]): void {
	const date = new Date();
	console.log(`${date.toLocaleString()} [LOG] ${args.join(' ')}`);
}

chrome.runtime.onMessage.addListener(
	(message: ContentScriptMessage | PopUpScriptMessage, _, sendResponse) => {
		let typed_message: ContentScriptMessage | PopUpScriptMessage;
		
		typed_message = message as ContentScriptMessage;
		if (typed_message.NewUrl) {
			INTERN_LIST.push(typed_message.NewUrl);
			backgroundLog('ADDED:', typed_message.NewUrl, 'LIST:', INTERN_LIST);
			sendResponse('added');
			chrome.runtime.sendMessage<BackgroundScriptMessage>(
				{ addNewUrl: typed_message.NewUrl },
				function(response) {
					backgroundLog('RESPONSE of add in popup:', response);
				},
			);
			return;
		}
		
		typed_message = message as PopUpScriptMessage;
		if (typeof typed_message.action === 'string') {
			switch (typed_message.action) {
				case 'removeLast':
					INTERN_LIST.pop();
					sendResponse('removed last item');
					backgroundLog('REMOVED LAST');
					return;
				case 'clear':
					INTERN_LIST = [];
					sendResponse('cleared');
					backgroundLog('CLEARED');
					return;
				case 'list':
					sendResponse(INTERN_LIST);
					backgroundLog('LIST', INTERN_LIST);
					return;
				default:
					return;
			}
		}
		
		if (Array.isArray(typed_message.action)) {
			if (typed_message.action[0] === 'removeElement') {
				const index = Number(typed_message.action[1]);
				if (isNaN(index) || index < 0 || index >= INTERN_LIST.length) {
					throw new Error('Invalid index');
				}
				INTERN_LIST.splice(index, 1);
				sendResponse('removed element');
				backgroundLog('REMOVED ELEMENT:', typed_message.action[1]);
			}
		}
	},
);

export {};
