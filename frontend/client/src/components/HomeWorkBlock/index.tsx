import React from 'react';
import styles from './HomeWorkBlock.module.scss';

interface HomeWorkBlockProps {
  control: boolean;
  complete: boolean;
  time?: boolean;
}
const HomeWorkBlock: React.FC<HomeWorkBlockProps> = ({ control, complete, time }) => {
  return (
    <div className={styles.block}>
      <div className={styles.items}>
        <div className={styles.information}>
          <div className={styles.avatar}>
            <span></span>
          </div>
          <div className={styles.about}>
            <div className={styles.name}>Алгебра</div>
            {time ? <div>кабинет, время</div> : <div className={styles.work}>параграф, 18</div>}
          </div>
        </div>
        {complete ? (
          <form action="">
            <input type="checkbox" className={styles.complete} id="complete" />
            <label htmlFor="complete"></label>
          </form>
        ) : control ? (
          <div>Дата публикации</div>
        ) : (
          ''
        )}
      </div>
    </div>
  );
};

export default HomeWorkBlock;
