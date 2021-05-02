import React from 'react';
import { useRoutes } from 'react-router-dom';
import { ThemeProvider } from '@material-ui/core';
import routes from './routes';

require('dotenv').config();

const App = () => {
  const routing = useRoutes(routes);

  return (
    <ThemeProvider key={1}>
      {routing}
    </ThemeProvider>
  );
};

export default App;
