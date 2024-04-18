import React, { useState } from 'react';
import styles from './Navigation.module.scss';
import { Link, NavLink } from 'react-router-dom';
import classNames from 'classnames';

type RouteItem = {
  name: string;
  path: string;
};
const Navigation: React.FC = () => {
  const routeList: RouteItem[] = [
    { name: 'Главная', path: '/home' },
    { name: 'Оценки', path: '/grade' },
  ];
  function getClassName({ isActive }: { isActive: boolean }): string {
    return classNames(styles.link, {
      [styles.active]: isActive,
    });
  }
  return (
    <ul className={styles.menu}>
      {routeList.map((el, i) => (
        <li key={el.path} className={styles.item}>
          <NavLink to={el.path} className={getClassName}>
            {el.name}
          </NavLink>
        </li>
      ))}
    </ul>
  );
};

export default Navigation;
