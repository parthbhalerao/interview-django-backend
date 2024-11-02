import { createTheme } from '@mui/material/styles';
import { brand, gray, green, orange, red } from './base/colors';
import { typography } from './base/typography';
import { shadows } from './base/shadows';
import { shape } from './base/shape';

export const baseTheme = createTheme({
  typography,
  shape,
  shadows,
  palette: {
    primary: {
      ...brand,
      light: brand[200],
      main: brand[400],
      dark: brand[700],
      contrastText: brand[50],
    },
    info: {
      ...brand,
      light: brand[100],
      main: brand[300],
      dark: brand[600],
      contrastText: gray[50],
    },
    warning: {
      ...orange,
      light: orange[300],
      main: orange[400],
      dark: orange[800],
    },
    error: {
      ...red,
      light: red[300],
      main: red[400],
      dark: red[800],
    },
    success: {
      ...green,
      light: green[300],
      main: green[400],
      dark: green[800],
    },
    grey: {
      ...gray,
    },
  },
});

export default baseTheme; 