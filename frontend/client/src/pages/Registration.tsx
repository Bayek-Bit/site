import React from 'react';

import { observer } from 'mobx-react';

import Auth from '../modules/Registration/components/Auth/Auth';

const Registration: React.FC = () => {
  return (
    <div className="registration">
      <Auth />
    </div>
  );
};

export default observer(Registration);
