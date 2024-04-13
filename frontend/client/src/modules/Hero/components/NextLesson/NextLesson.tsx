import React from 'react';
import styles from './NextLesson.module.scss';
import HomeWorkBlock from '../../../../components/HomeWorkBlock';

const NextLesson: React.FC = (props) => {
  return (
    <div className={styles.block}>
      <div className={styles.title}>Следующий урок:</div>
      <HomeWorkBlock time />
    </div>
  );
};

export default NextLesson;
