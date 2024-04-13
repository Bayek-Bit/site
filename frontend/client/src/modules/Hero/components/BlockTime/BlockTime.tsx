import React from 'react';
import TimeNow from '../../../../components/TimeNow';
import LessonNumber from '../../../../components/LessonNumber';
import styles from './BlockTime.module.scss';
const BlockTime: React.FC = () => {
  return (
    <div className={styles.block}>
      <div className={styles.items}>
        <TimeNow />
        <LessonNumber />
      </div>
    </div>
  );
};

export default BlockTime;
