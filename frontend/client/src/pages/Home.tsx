import React from 'react';

import { Header } from '../modules/Header/index';
import { Hero } from '../modules/Hero/index';
import { Advert } from '../modules/Advert/index';
import { Tasks } from '../modules/Tasks/index';
import { Greeting } from '../modules/Greeting/index';
import { Calendar } from '../modules/Calendar/index';
import { TodayLessons } from '../modules/TodayLessons';
import MainLayout from '../layouts/MainLayout';

const Home: React.FC = () => {
  return (
    <>
      <MainLayout>
        <Greeting />
        <Hero />
        <Tasks />
        <Advert />
      </MainLayout>
    </>
  );
};

export default Home;
