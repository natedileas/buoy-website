import React from 'react';

export class Header extends React.Component {
  render() {
    return <div id="header">
      <h1>
        <a href="http://127.0.0.1:5000/index">Home</a> |
        <a href="http://127.0.0.1:5000/process">Process</a> |
        <a href="http://127.0.0.1:5000/jobs">Jobs</a> |
        <a href="http://cis.rit.edu">CIS</a> |
        <a href="http://rit.edu">RIT</a>
      </h1>
    </div>;
  }
}
