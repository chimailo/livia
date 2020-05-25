import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { MuiThemeProvider } from '@material-ui/core';
import CssBaseline from '@material-ui/core/CssBaseline';

import Firebase, { FirebaseContext } from './Firebase';
import { theme } from './utils/theme';
import store from './store';
import * as serviceWorker from './serviceWorker';

const render = () => {
  const App = require('./components/App').default;

  ReactDOM.render(
    <React.StrictMode>
      <MuiThemeProvider theme={theme}>
        <FirebaseContext.Provider value={new Firebase()}>
          <CssBaseline />
          <Provider store={store}>
            <App />
          </Provider>
        </FirebaseContext.Provider>
      </MuiThemeProvider>
    </React.StrictMode>,
    document.getElementById('root')
  );
};

render();

if (process.env.NODE_ENV === 'development' && module.hot) {
  module.hot.accept('./components/App', render);
}

serviceWorker.unregister();
