import React from 'react';
import styles from './Logo.module.scss';
import { Link } from 'react-router-dom';

const Logo: React.FC = () => {
  return (
    <div className={styles.logo}>
      <Link to="/home"> School Diary </Link>
    </div>
  );
};

export default Logo;
