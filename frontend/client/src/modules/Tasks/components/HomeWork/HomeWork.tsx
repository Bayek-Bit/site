import React from 'react';
import HomeWorkBlock from '../../../../components/HomeWorkBlock';
import styles from './HomeWork.module.scss';
type HomeWorkProps = {
  value: boolean | any;
  title: string | any;
};
const HomeWork: React.FC<HomeWorkProps> = ({ value, title }) => {
  const type = value ? true : false;
  return (
    <div className={styles.main}>
      <div className={styles.title}>{title}</div>
      <div className={styles.items}>
        <div className={styles.block}>
          <HomeWorkBlock complete={type} control={value ? false : true} />
        </div>
        <div className={styles.block}>
          <HomeWorkBlock complete={type} control={value ? false : true} />
        </div>
        <div className={styles.block}>
          <HomeWorkBlock complete={type} control={value ? false : true} />
        </div>
        <div className={styles.block}>
          <HomeWorkBlock complete={type} control={value ? false : true} />
        </div>
      </div>
    </div>
  );
};

export default HomeWork;
