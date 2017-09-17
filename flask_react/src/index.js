import React from 'react';
import ReactDOM from 'react-dom';

import {Header} from './components/header.js';
import {LandsatForm} from './components/form.js';
import {Jobs} from './components/jobs.js';

import './index.css';

const Main = () => (
    <div>
      <Header/>
      <LandsatForm/>
      <Jobs/>
    </div>
);

ReactDOM.render(React.createElement(Main), document.getElementById('root'));
