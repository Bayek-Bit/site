import React from 'react';
import styles from './Greeting.module.scss';
import student from './assets/student.png';
const GreetingBlock: React.FC = (props) => {
  return (
    <div className={styles.block}>
      <div className={styles.items}>
        <div className={styles.image}>
          <img src={student} alt="" />
        </div>
        <div className={styles.information}>
          <div className={styles.title}>Привет, Имя</div>
          <div className={styles.hello}>Добро пожаловать в электронный дневник</div>
          <div className={styles.text}>
            Многофункциональный клиент для электронного дневника вашей школы
          </div>
        </div>
      </div>
    </div>
  );
};

export default GreetingBlock;
