import React from 'react';
import styles from './Calendar.module.scss';
const Calendar: React.FC = () => {
  const months = [
    'Январь',
    'Февраль',
    'Март',
    'Апрель',
    'Май',
    'Июнь',
    'Июль',
    'Август',
    'Сентябрь',
    'Октябрь',
    'Ноябрь',
    'Декабрь',
  ];
  const date = new Date();
  const month = date.getMonth();
  const year = date.getFullYear();

  const start = new Date(year, month, 1).getDay();
  const endDate = new Date(year, month + 1, 0).getDay();

  const end = new Date(year, month, endDate).getDay();
  const endDatePrev = new Date(year, month, 0).getDay();

  return (
    <div className={styles.calendar}>
      <header>
        <h3>Календарь</h3>
        <p>{months[month]}</p>
      </header>
      <section>
        <ul className={styles.days}>
          <li>Пн</li>
          <li>Вт</li>
          <li>Ср</li>
          <li>Чт</li>
          <li>Пт</li>
          <li>Сб</li>
          <li>Вс</li>
        </ul>
        <ul className={styles.dates}></ul>
      </section>
    </div>
  );
};

export { Calendar };
