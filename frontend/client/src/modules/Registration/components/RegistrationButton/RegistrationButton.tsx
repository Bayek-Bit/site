import React from 'react';
import styles from './RegistrationButton.module.scss';
const RegistrationButton = ({ children, ...props }) => {
  return (
    <button {...props} className={styles.myBtn}>
      {children}
    </button>
  );
};

export default RegistrationButton;
