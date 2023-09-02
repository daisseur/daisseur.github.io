Chrome extension
===
---

# Build

Typescript check: `npm run check`

Then run `npm build`

The generated files are in the `dist` folder.

# Usage

## Chrome

Go to `chrome://extensions/` url and enable developer mode.

Then click on `Load unpacked` and select the `dist` folder.

# Warning

All the code must be standalone inside each `page` folder.
Only shared types imports are allowed, because they are removed during the build process.
Otherwise, it will break the extension.

# Inspiration

https://github.com/JohnBra/vite-web-extension
