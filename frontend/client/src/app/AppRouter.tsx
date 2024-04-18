import React, { useContext, useEffect } from 'react';
import { observer } from 'mobx-react';
import Registration from '../pages/Registration';
import { privateRoutes, publicRoutes } from '../router/routes';
import { Navigate, Route, Routes } from 'react-router-dom';
import { Context } from '../main';
import Home from '../pages/Home';
import Grade from '../pages/Grade';

function AppRouter() {
  const { store } = useContext(Context);

  useEffect(() => {
    if (localStorage.getItem('token')) {
      store.checkAuth();
    }
  }, []);
  console.log(store.isAuth);
  if (!store.isAuth) {
    return <Registration />;
  }

  return store.isAuth ? (
    <Routes>
      <Route element={<Home />} path={privateRoutes[0].path} key={privateRoutes[0].path} />
      <Route element={<Grade />} path={privateRoutes[1].path} key={privateRoutes[1].path} />
      <Route path="/*" element={<Navigate to="/home"></Navigate>}></Route>
    </Routes>
  ) : (
    <Routes>
      <Route element={<Registration />} path={publicRoutes[0].path} key={publicRoutes[0].path} />
      <Route path="/*" element={<Navigate to="/login"></Navigate>}></Route>
    </Routes>
  );
}

export default observer(AppRouter);
