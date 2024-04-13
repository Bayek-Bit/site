import React from 'react';
import styles from './AdvertBlock.module.scss';
const AdvertBlock: React.FC = () => {
  return (
    <div className={styles.block}>
      <div className={styles.items}>
        <div className={styles.header}>
          <div className={styles.information}>
            <div className={styles.avatar}></div>
            <div className={styles.name}>fdffd fdfdfdfd fdfdfdfd dfdfd</div>
          </div>

          <div className={styles.date}>Сегодня</div>
        </div>
        <div className={styles.title}>
          Lorem ipsum dolor sit, amet consectetur adipisicing elit. Unde natus minus rem quibusdam
          deleniti.
        </div>
        <div className={styles.text}>
          Lorem ipsum dolor sit, amet consectetur adipisicing elit. Unde natus minus rem quibusdam
          deleniti.
        </div>
      </div>
    </div>
  );
};

export default AdvertBlock;
