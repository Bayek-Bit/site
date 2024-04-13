import React from 'react';
import Logo from '../../../../UI/Logo/Logo';
import Navigation from '../../../../components/Navigation';
import Burger from '../Burger/Burger';
import styles from './Header.module.scss';
import Profile from '../../../../components/Profile';
const Header: React.FC = () => {
  return (
    <nav>
      <div className="container">
        <div className={styles.navbar}>
          <Logo />
          <Navigation />
          <Profile />
          <Burger />
        </div>
      </div>
    </nav>
  );
};

export { Header };
