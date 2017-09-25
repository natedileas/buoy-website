import React from 'react';
import axios from 'axios';
import { Form, Grid, Image } from 'semantic-ui-react';

import 'semantic-ui-css/semantic.min.css';


export class LandsatForm extends React.Component {
  constructor(args) {
      super();
      this.state = {
          scene_id: "",
          thumbnail_url: "",
          thumbnail_url_2: "",
          buoys: [],
          buoy: "",
          atmo: ""
      }
  }

  scene_id_change(event) {
    let id = event.target.value;
    this.setState({scene_id: id});

    let _thumbnail_url = "";

  	if (id.length === 21){ // it's a landsat 8 pre-collection id
  		let path = id.substring(3, 6);
  		let row = id.substring(6, 9);
  		let year = id.substring(9, 13);
  		_thumbnail_url = 'https://earthexplorer.usgs.gov/browse/landsat_8/' + year + '/' + path + '/' + row + '/' + id + '.jpg'
  	}
  	else if (id.length === 40) { // it's a landsat 8 collection 1 id
  		let path = id.substring(10, 13);
  		let row = id.substring(13, 16);
  		let year = id.substring(17, 21);
  		_thumbnail_url = 'https://earthexplorer.usgs.gov/browse/landsat_8/' + year + '/' + path + '/' + row + '/' + id + '.jpg'
  	}

    if (_thumbnail_url !== ""){
      console.log(_thumbnail_url);
      this.setState({thumbnail_url: _thumbnail_url, scene_id: id},
        () => {
           this.update_buoy_ids(id);
           this.update_atmo_preview();
         });
    }
  }

  update_buoy_ids (id) {
    let url = 'http://localhost:5000/buoys?id=' + id;
    var self = this;

    axios.get(url).then(function (response) {

      console.log(response);

      let _buoys = response['data']['buoys'];
      let buoy_options = [];
      for (var i=0; i<_buoys.length; i++){
        buoy_options.push(<option key={_buoys[i]} value={_buoys[i]}>{_buoys[i]}</option>);
      }

      self.setState({buoys: buoy_options});
    });
  }

  buoy_change (event) {
    this.setState({buoy: event.target.value});
  }

  atmo_change(event) {
    this.setState({atmo: event.target.value},
      () => {
         this.update_atmo_preview();
       });
  }

  update_atmo_preview() {
    let url = 'http://localhost:5000/preview';
    var self = this;

    axios.post(url, this.state).then(function (response) {
      console.log(response);
      self.setState({thumbnail_url: response.data['preview_image']});
    });
  }

  onsubmit () {
    // post form data and start backgorund task
    var self = this;
    let url = 'http://localhost:5000/new_task';

    // TODO add content checkss

    axios.post(url, self.state).then(function (response) {
      console.log(response);
    });
    self.setState({scene_id:"", thumbnail_url: "", buoys: []});
  }

  render() {
    return (
      <Grid columns={2} divided >
        <Grid.Row>
          <Grid.Column width={5} className="form side">
            <Form onSubmit={(e) => {e.preventDefault(); this.onsubmit()}}>
              <label> Scene ID:</label>
              <input type="text" name="scene_id" value={this.state.scene_id} onChange={this.scene_id_change.bind(this)} size="45"/>
              <label> Atmosphere Source:</label>
              <select name="atmo" value={this.state.atmo} onChange={this.atmo_change.bind(this)}>
                <option value="merra">MERRA-2</option>
                <option value="narr">NARR-2</option>
              </select>
              <label> Buoy ID:</label>
              <select name="buoy" onChange={this.buoy_change.bind(this)} >
                {this.state.buoys}
              </select>
              <Form.Button type='submit'>Submit</Form.Button>
            </Form>
          </Grid.Column>
          <Grid.Column width={5}>
            <label>Scene Preview:</label>
            <Image src={this.state.thumbnail_url} width="300" height="300"/>
          </Grid.Column>
        </Grid.Row>
      </Grid>
    )
  }
}
