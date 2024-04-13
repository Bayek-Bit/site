import React from 'react';

import { Header } from '../modules/Header/index';
import { Hero } from '../modules/Hero/index';
import { Advert } from '../modules/Advert/index';
import { Tasks } from '../modules/Tasks/index';
import { Greeting } from '../modules/Greeting/index';
import { Calendar } from '../modules/Calendar/index';
import { TodayLessons } from '../modules/TodayLessons';

const Home: React.FC = () => {
  return (
    <>
      <Header />
      <div className="container">
        <div className="main">
          <div className="wrapper">
            <Greeting />
            <Hero />
            <Tasks />
            <Advert />
          </div>
          <div className="calendar">
            <Calendar />
            <TodayLessons />
          </div>
        </div>
      </div>
    </>
  );
};

export default Home;
