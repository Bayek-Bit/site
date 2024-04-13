import React from 'react';
import AdvertBlock from '../../../../components/AdvertBlock';
import styles from './Advert.module.scss';
const Advert: React.FC = () => {
  return (
    <div className={styles.advert}>
      <div className="container">
        <div className={styles.title}>Новые объявления</div>
        <div className={styles.items}>
          <div className={styles.block}>
            <AdvertBlock />
          </div>
          <div className={styles.block}>
            <AdvertBlock />
          </div>
          <div className={styles.block}>
            <AdvertBlock />
          </div>
          <div className={styles.block}>
            <AdvertBlock />
          </div>
        </div>
      </div>
    </div>
  );
};

export { Advert };
