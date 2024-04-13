import React from 'react';
import Date from '../../components/Date';
import BlockTime from './components/BlockTime/BlockTime';
import styles from './Hero.module.scss';
import NextLesson from './components/NextLesson/NextLesson';
const Hero: React.FC = () => {
  return (
    <div className={styles.hero}>
      <div className={`container `}>
        <div className={styles.content}>
          <div className={styles.time}>
            <div className={styles.title}>Время:</div>
            <BlockTime />
          </div>
          <div className={styles.lesson}>
            <NextLesson />
          </div>
        </div>
      </div>
    </div>
  );
};

export { Hero };
