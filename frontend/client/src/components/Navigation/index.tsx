import React, { useState } from 'react';
import styles from './Navigation.module.scss';
import { Link } from 'react-router-dom';

type RouteItem = {
  name: string;
  path: string;
};
const Navigation: React.FC = () => {
  const [categoryId, setCategoryId] = useState(0);
  const onClickCategory = (id: number) => {
    setCategoryId(id);
  };

  const routeList: RouteItem[] = [
    { name: 'Главная', path: '/' },
    { name: 'Оценки', path: '/grade' },
  ];

  return (
    <ul className={styles.menu}>
      {routeList.map((el, i) => (
        <li key={el.name} onClick={() => onClickCategory(i)} className={styles.link}>
          <Link to={el.path} className={`${styles.link} ${categoryId == i ? styles.active : ''}`}>
            {el.name}
          </Link>
        </li>
      ))}
    </ul>
  );
};

export default Navigation;
