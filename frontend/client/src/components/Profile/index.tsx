import React, { useContext } from 'react';
import styles from './Profile.module.scss';
import logout from './assets/logout.svg';
import { Context } from '../../main';
import { observer } from 'mobx-react';
const Profile: React.FC = () => {
  const { store } = useContext(Context);
  return (
    <div className={styles.profile}>
      <span className={styles.avatar}></span>
      <a className={styles.name} href="">
        Profile Name, grade
      </a>
      <div onClick={() => store.logout()} className={styles.logout}>
        <img className={styles.img} src={logout} alt="" />
      </div>
    </div>
  );
};

export default observer(Profile);
