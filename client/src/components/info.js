import React from 'react';
import { Container } from 'semantic-ui-react';

import 'semantic-ui-css/semantic.min.css';

export class Info extends React.Component {
  state = {}

  handleItemClick = (e, { name }) => this.setState({ activeItem: name })

  render() {
    const { activeItem } = this.state

    return (<Container>
      <h3>Overview:</h3>
      <p>
      Calculates and compares the radiance of a thermal LANDSAT scene to the ground truth radiance as measured by a NOAA buoy and atmospheric propogation using MODTRAN, NARR, and/or MERRA. Based on work by Frank Padula and Monica Cook. <br/><br/>This code essentially has two funtions: calculating the radiance from the landsat image provided, and calculating the corresponding ground truth radiance from outside data,atmospheric (NARR or MERRA-2), NOAA buoy data, and MODTRAN.
      <br/> To use this tool, fill out the form, then 
      </p>

      <h4>Data Sources:</h4>
      <h5>NARR:</h5><p>
          This is the primary atmospheric data source for the project. Height, Temperature, Humidity as a funtion of Pressure. <br/>
          NCEP Reanalysis data provided by the NOAA/OAR/ESRL PSD, Boulder, Colorado, USA, from their Web site at <a href="http://www.esrl.noaa.gov/psd/">esrl.noaa.gov/psd/</a><br/><br/>

          Website: <a href="http://www.esrl.noaa.gov/psd/data/gridded/data.narr.html">esrl.noaa.gov/psd/data/gridded/data.narr.html</a><br/>
          FTP: <a href="ftp://ftp.cdc.noaa.gov/Datasets/NARR/pressure/">ftp.cdc.noaa.gov/Datasets/NARR/pressure/</a>
      </p>
      <h5>MERRA:</h5><p>
          This is the secondary atmospheric data source for the project. Height, Temperature,
          Humidity as a funtion of Pressure. It was instituted as a result of the NARR dataset
          not being up to date. Until late 2016, the NARR archive only reaches to late 2014.<br/><br/>

          Website: <a href="http://gmao.gsfc.nasa.gov/reanalysis/MERRA-2/">gmao.gsfc.nasa.gov/reanalysis/MERRA-2/</a><br/>
          FTP: <a href="ftp://goldsmr5.sci.gsfc.nasa.gov/data/s4pa/MERRA2/M2I3NPASM.5.12.4/">goldsmr5.sci.gsfc.nasa.gov/data/s4pa/MERRA2/M2I3NPASM.5.12.4/</a>
      </p>

      <h5>NOAA:</h5><p>
          This is the only source of water temperature information for the project.<br/><br/>

          Website: <a href="http://www.ndbc.noaa.gov/">ndbc.noaa.gov/</a><br/>
          Data: <a href="http://www.ndbc.noaa.gov/data/stations/station_table.txt">ndbc.noaa.gov/data/stations/station_table.txt</a><br/>
              <a href="http://www.ndbc.noaa.gov/data/stdmet/">ndbc.noaa.gov/data/stdmet/</a><br/>
              <a href="http://www.ndbc.noaa.gov/data/historical/stdmet/">ndbc.noaa.gov/data/historical/stdmet/</a>
      </p>

      <h4>References:</h4>
      <p>
          <a href="http://scholarworks.rit.edu/theses/2961/">Frank Padula's Thesis (08)</a><br/>
          <a href="http://scholarworks.rit.edu/theses/8513/">Monica Cook's Thesis (12)</a><br/>
      </p>
  </Container>
  )
  }
}
