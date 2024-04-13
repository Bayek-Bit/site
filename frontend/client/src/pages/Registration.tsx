import React, { useContext, useEffect } from 'react';
import { Context } from '../main';
import { observer } from 'mobx-react';
import { useNavigate } from 'react-router-dom';
import Auth from '../modules/Registration/components/Auth/Auth';

const Registration: React.FC = () => {
  const { store } = useContext(Context);
  const navigate = useNavigate();

  useEffect(() => {
    if (localStorage.getItem('token')) {
      store.checkAuth();
    }
    
    if (store.isAuth) {
      navigate('/home');
    }
  }, [store.isAuth, navigate, store]);

  console.log(store.isAuth);
  
  return (
    <div className="registration">
      <Auth />
    </div>
  );
};

export default observer(Registration);