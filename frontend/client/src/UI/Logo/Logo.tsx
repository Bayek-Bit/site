import React from 'react';
import styles from './Logo.module.scss';

const Logo: React.FC = () => {
  return (
    <div className={styles.logo}>
      <a href="/"> School Diary </a>
    </div>
  );
};

export default Logo;
