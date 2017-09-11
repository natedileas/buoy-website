import React from 'react';
import axios from 'axios';

export class LandsatForm extends React.Component {
  constructor(args) {
      super();
      this.state = {
          scene_id: "",
          thumbnail_url: "",
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

    console.log(this.state);
    axios.post(url, this.state).then(function (response) {
      console.log(response);
      self.setState({thumbnail_url: response.data['preview_image']});
    });
  }

  onsubmit () {
    // post form data and start backgorund task
    // TODO
    let url = 'http://localhost:5000/submit';
    var self = this;

    axios.post(url, self.state).then(function (response) {
      console.log(response);
    });
  }

  render() {
    return <div id="form">
    <form onSubmit={this.onsubmit}>
    <p> Scene ID:
    <input type="text" name="scene_id" value={this.state.scene_id} onChange={this.scene_id_change.bind(this)}/>
    <br/> Atmosphere Source
    <select name="atmo" value={this.state.atmo} onChange={this.atmo_change.bind(this)}>
      <option value="merra">MERRA-2</option>
      <option value="narr">NARR-2</option>
    </select>
    <br/> Buoy ID:
    <select name="buoy" onChange={this.buoy_change.bind(this)}>
      {this.state.buoys}
    </select>
    <br/>
    <input type="submit" value="Submit"/>
    </p>
    </form>

    <img src={this.state.thumbnail_url} width="300" height="300" alt="scene preview"/>
    </div>;
  }
}
