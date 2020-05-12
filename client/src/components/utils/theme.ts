import { createMuiTheme } from '@material-ui/core';

export const theme = createMuiTheme({
  palette: {
    primary: {
      main: '#226089',
    },
    secondary: {
      main: '#e2f3f5',
    },
    // type: 'dark',
  },
  mixins: {
    toolbar: {
      minHeight: '52px',
    },
  },
  typography: {
    h1: {
      fontSize: '3.5rem',
    },
    h2: {
      fontSize: '3rem',
    },
    h3: {
      fontSize: '2.5rem',
    },
    h4: {
      fontSize: '2rem',
    },
    h5: {
      fontSize: '1.75rem',
    },
    h6: {
      fontSize: '1.5rem',
    },
  },
});
