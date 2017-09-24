import React from 'react';
import axios from 'axios';
import { Container } from 'semantic-ui-react';


var URL = 'http://localhost:5000/';

export class Jobs extends React.Component {
  constructor(args) {
      super();
      this.state = {
        "jobs": []
      }

      this.update = this.update.bind(this);
      this.interval = setInterval(this.update, 5000);
  }

  update() {
    var self = this;

    axios.get(URL+'enum_tasks').then(function (response) {
      console.log(response);
      self.setState({jobs: response.data.jobs});
    });
  }

  render() {
    this.update();
    
    return (
      <Container>
      <h1>Jobs:</h1>
      {this.state.jobs.map(job =>
        <Job key={job.id} id={job.id}/>
      )}
    </Container>)
  }
}

class Job extends React.Component {
  constructor(props) {
      super(props);
      this.state = {
        status: "",
        id: this.props.id,
        url: URL + 'status/' + this.props.id,
      }

      this.update = this.update.bind(this);
      this.interval = setInterval(this.update, 1000);
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }

  update() {
    var self = this;

    axios.get(self.state.url).then(function (response) {
      console.log(response);
      let state = response.data.state;
      self.setState({status:state});
      if (state === 'SUCCESS'){
        clearInterval(self.interval);
      }
    });
  }

  render () {

    return (<Container className="job">
          <h3>{this.state.id}</h3>
          Status: {this.state.status}
      </Container>)
  }
}
