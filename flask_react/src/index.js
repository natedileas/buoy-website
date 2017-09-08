import React from 'react';
import ReactDOM from 'react-dom';

const BasicExample = () => (
    <div>
      <h2> Hello world </h2>
    </div>
);

ReactDOM.render(React.createElement(BasicExample), document.getElementById('root'));
