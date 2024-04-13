import React from 'react';
import HomeWork from './components/HomeWork/HomeWork';
import styles from './Tasks.module.scss';

const Tasks: React.FC = () => {
  return (
    <div className={styles.tasks}>
      <div className="container">
        <div className={styles.content}>
          <div className={styles.work}>
            <HomeWork value={true} title="Домашнее задание" />
          </div>
          <div className={styles.control}>
            <HomeWork value={false} title="Контрольные работы" />
          </div>
        </div>
      </div>
    </div>
  );
};

export { Tasks };
