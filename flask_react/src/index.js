import React from 'react';
import ReactDOM from 'react-dom';

import {Header} from './components/header.js';
import {LandsatForm} from './components/form.js';

import './index.css';

const BasicExample = () => (
    <div>
      <Header/>
      <LandsatForm/>
    </div>
);

ReactDOM.render(React.createElement(BasicExample), document.getElementById('root'));
