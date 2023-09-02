export type BackgroundScriptMessage = {
	addNewUrl: string;
};
export type ContentScriptMessage = {
	NewUrl: string;
};
export type PopUpScriptMessage = {
	action: string | string[];
};