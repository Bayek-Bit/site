import React from 'react';
import styles from './RegistrationAuthForm.module.scss';

type RegistrationAuthFormProps = {
  placeholder: string;
  type: string;
  name: string;
};
const RegistrationAuthForm: React.FC<RegistrationAuthFormProps> = ({
  placeholder,
  type,
  name,
  ...props
}) => {
  return (
    <div>
      <input
        name={name}
        placeholder={placeholder}
        type={type}
        className={styles.myInput}
        {...props}
      />
    </div>
  );
};

export default RegistrationAuthForm;
