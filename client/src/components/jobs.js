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
      this.update();
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
        name: "",
        message: "",
        returns: "",
        url: URL + 'status/' + this.props.id,
      }

      this.update = this.update.bind(this);
      this.update();
      this.interval = setInterval(this.update, 1000);
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }

  update() {
    var self = this;

    axios.get(self.state.url).then(function (response) {
      console.log(response);

      if (response.data.state === 'SUCCESS'){
        clearInterval(self.interval);
      }

      if(typeof response.data.config != "undefined"){
        let _name = response.data.config.scene_id;
        self.setState({name: _name});
      }


      self.setState({status: response.data.state,
                  message: response.data.message,
                  returns: response.data.returns
                  });
    });
  }

  render () {

    return (<Container className="job">
          <h3>{this.state.name}</h3>
          ID: {this.state.id}<br/>
          Status: {this.state.status}<br/>
          Message: {this.state.message}<br/>
          Returns: {this.state.returns}
          <hr/>
      </Container>)
  }
}
