import React from 'react';
import ReactDOM from 'react-dom';
import { MuiThemeProvider } from '@material-ui/core';
import CssBaseline from '@material-ui/core/CssBaseline';

import App from './components/App';
import Firebase, { FirebaseContext } from './Firebase';
import { theme } from './components/utils/theme';
import * as serviceWorker from './serviceWorker';

console.log(theme);

ReactDOM.render(
  <React.StrictMode>
    <MuiThemeProvider theme={theme}>
      <FirebaseContext.Provider value={new Firebase()}>
        <CssBaseline />
        <App />
      </FirebaseContext.Provider>
    </MuiThemeProvider>
  </React.StrictMode>,
  document.getElementById('root')
);

serviceWorker.unregister();
