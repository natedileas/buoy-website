import React from 'react';
import ReactDOM from 'react-dom';

import {Info} from './components/info.js';
import {LandsatForm} from './components/form.js';
import {Jobs} from './components/jobs.js';

import { Container, Menu, Image, Header} from 'semantic-ui-react';

import './index.css';
import {BrowserRouter as Router, Route} from 'react-router-dom'

let activeItem = window.location.pathname;

const Root = () => (
    <Router>
        <div>
            <Container>
                <Image src="https://www.cis.rit.edu/sites/cis.rit.edu/files/documents/materials-and-publications/CIS_horizontal.gif"/>
                <Header as='h1' textAlign='center'>Buoy Calibration</Header>
                <Menu pointing secondary>
                    <Menu.Item name='home' active={activeItem.includes('home')} href="/"/>
                    <Menu.Item name='form' active={activeItem.includes('form')} href="/form"/>
                    <Menu.Item name='jobs' active={activeItem.includes('jobs')} href="/jobs"/>
                    <Menu.Item name='CIS' active={activeItem.includes('CIS')} href="http://cis.rit.edu"/>
                </Menu>
                <Route exact path="/" component={Info}/>
                <Route exact path="/form" component={LandsatForm}/>
                <Route exact path="/jobs" component={Jobs}/>
            </Container>
        </div>
    </Router>
);

ReactDOM.render(React.createElement(Root), document.getElementById('root'));
