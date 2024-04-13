import React, { useContext, useEffect, useState } from 'react';

import Logo from '../../../../UI/Logo/Logo';
import RegistrationAuthForm from '../RegistrationAuthForm/RegistrationAuthForm';
import RegistrationButton from '../RegistrationButton/RegistrationButton';
import styles from './Auth.module.scss';
import { Context } from '../../../../main';
import { observer } from 'mobx-react';
const Auth: React.FC = () => {
  const { store } = useContext(Context);
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [emailDirty, setEmailDirty] = useState<boolean>(false);
  const [passwordDirty, setPasswordDirty] = useState<boolean>(false);
  const [emailError, setEmailError] = useState<string>('Email не может быть пустым');
  const [passwordError, setPasswordError] = useState<string>('Password не может быть пустым');
  const [formValid, setFormValid] = useState<boolean>(false);

  useEffect(() => {
    if (emailError || passwordError) {
      setFormValid(false);
    } else {
      setFormValid(true);
    }
  }, [emailError, passwordError]);
  const emailHandler = (e: any) => {
    setEmail(e.target.value);
    const re =
      /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
    if (!re.test(String(e.target.value).toLowerCase())) {
      setEmailError('Некоректный email');
    } else {
      setEmailError('');
    }
  };

  const passwordHandler = (e: any) => {
    setPassword(e.target.value);
    if (e.target.value.length < 6 || e.target.value.length > 16) {
      setPasswordError('Пароль должен быть длиннее 3 и меньше 16 символов');
      if (!e.target.value) {
        setPasswordError('Password не может быть пустым');
      }
    } else {
      setPasswordError('');
    }
  };
  const blurHandle = (e: any) => {
    switch (e.target.name) {
      case 'email':
        setEmailDirty(true);
        break;
      case 'password':
        setPasswordDirty(true);
        break;
    }
  };
  return (
    <div className={styles.main}>
      <div>
        <div className={styles.logo}>
          <Logo />
        </div>
        <div className={styles.email}>
          {emailDirty && emailError && (
            <div style={{ color: 'red', fontFamily: 'Montserrat' }}>{emailError}</div>
          )}
          <RegistrationAuthForm
            value={email}
            onChange={(e: any) => emailHandler(e)}
            onBlur={(e: any) => blurHandle(e)}
            name={'email'}
            placeholder={'Email'}
            type={'text'}
          />
        </div>
        <div className={styles.password}>
          {passwordDirty && passwordError && (
            <div style={{ color: 'red', fontFamily: 'Montserrat' }}>{passwordError}</div>
          )}
          <RegistrationAuthForm
            value={password}
            onChange={(e: any) => passwordHandler(e)}
            onBlur={(e: any) => blurHandle(e)}
            name={'password'}
            placeholder={'Password'}
            type={'password'}
          />
        </div>
        <div className={styles.btn}>
          <RegistrationButton onClick={() => store.login(email, password)} disabled={!formValid}>
            Войти
          </RegistrationButton>
        </div>
      </div>
    </div>
  );
};

export default observer(Auth);
