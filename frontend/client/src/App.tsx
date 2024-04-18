import React, { useContext, useEffect } from 'react';
import { Route, Routes, BrowserRouter } from 'react-router-dom';

import AppRouter from './app/AppRouter';
import './app/styles/style.scss';
import { Context } from './main';
const App: React.FC = () => {
  const { store } = useContext(Context);
  useEffect(() => {
    if (localStorage.getItem('auth')) {
      store.setAuth(true);
    }
  }, []);
  return (
    <>
      <BrowserRouter>
        <AppRouter />
      </BrowserRouter>
    </>
  );
};

export default App;
