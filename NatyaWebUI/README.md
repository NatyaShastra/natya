<<<<<<< HEAD
# natya
NatyaShastra is a community-driven dance academy dedicated to preserving and promoting the traditional art of Bharatanatyam. We offer both offline and online classes, making this timeless dance form accessible to all.
=======
# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type aware lint rules:

- Configure the top-level `parserOptions` property like this:

```js
export default tseslint.config({
  languageOptions: {
    // other options...
    parserOptions: {
      project: ["./tsconfig.node.json", "./tsconfig.app.json"],
      tsconfigRootDir: import.meta.dirname,
    },
  },
});
```

- Replace `tseslint.configs.recommended` to `tseslint.configs.recommendedTypeChecked` or `tseslint.configs.strictTypeChecked`
- Optionally add `...tseslint.configs.stylisticTypeChecked`
- Install [eslint-plugin-react](https://github.com/jsx-eslint/eslint-plugin-react) and update the config:

```js
// eslint.config.js
import react from "eslint-plugin-react";

export default tseslint.config({
  // Set the react version
  settings: { react: { version: "18.3" } },
  plugins: {
    // Add the react plugin
    react,
  },
  rules: {
    // other rules...
    // Enable its recommended rules
    ...react.configs.recommended.rules,
    ...react.configs["jsx-runtime"].rules,
  },
});
```
>>>>>>> 0b8f26b (All code chagnes)


[user]
    name = NatyaShastra
    email = natyashastra2018@gmail.com
    https://github.com/NatyaShastra/natya/tree/main/src

    # (1) Install Git if needed
git --version

# (2) Navigate to your project
cd path/to/your/project

# (3) Initialize Git and push to GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/NatyaShastra/natya.git
git branch -M main
git push -u origin main

# (4) Install Netlify CLI
npm install -g netlify-cli
netlify login

# (5) Build and Deploy React App
npm run build
netlify deploy
netlify deploy --prod


python --version
python -m venv rasa_env
rasa_env\Scripts\activate
pip install rasa
rasa init --no-prompt
rasa data validate
rasa train
rasa shell

To test if the Google Analytics tracking code is working correctly on your website, follow these steps:

Deploy Your Website:

Ensure that your website is deployed and accessible via a web server. If you are running it locally, make sure your local server is running.
Open Your Website:

Open your website in a web browser.
Check Real-Time Reports in Google Analytics:

Go to Google Analytics.
Navigate to the property you set up for your website.
Go to the "Real-Time" section in the left-hand menu.
Check the "Overview" page to see if your visit is being tracked.
Use Google Tag Assistant:

Install the Google Tag Assistant Chrome extension.
Open your website in a new tab.
Click on the Google Tag Assistant icon in the Chrome toolbar.
Enable the extension and refresh your website.
The extension will show you if the Google Analytics tag is firing correctly.
Check the Browser Console:

Open the Developer Tools in your browser (usually by pressing F12 or Ctrl+Shift+I).
Go to the "Console" tab.
Look for any errors related to the Google Analytics script.
By following these steps, you can verify that the Google Analytics tracking code is correctly integrated and tracking visitors to your website.