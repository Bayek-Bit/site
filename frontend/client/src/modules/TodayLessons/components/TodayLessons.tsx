import React from 'react';
import styles from './TodayLesson.module.scss';
import HomeWorkBlock from '../../../components/HomeWorkBlock';
const TodayLessons: React.FC = () => {
  return (
    <div className={styles.block}>
      <div className={styles.title}>Уроки</div>
      <HomeWorkBlock control={false} complete={false} time />
    </div>
  );
};

export { TodayLessons };
