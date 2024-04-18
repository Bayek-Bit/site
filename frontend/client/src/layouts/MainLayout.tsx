import React from 'react';
import { Header } from '../modules/Header/index';

import { Calendar } from '../modules/Calendar';
import { TodayLessons } from '../modules/TodayLessons';
import '../app/styles/style.scss';
function MainLayout({ children, ...props }) {
  return (
    <>
      <Header />
      <div className="container">
        <div className="main">
          <div className="wrapper">{children}</div>
          <div className="calendar">
            <Calendar />
            <TodayLessons />
          </div>
        </div>
      </div>
    </>
  );
}

export default MainLayout;
