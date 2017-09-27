import buoycalib
from app import celery

@celery.task(bind=True)
def calib_task(self, config):
    """

    Args:
        self: celery task object
        config: dict with name and options chosen
    """
    scene_id = config['scene_id']
    bands = [10, 11, 'MTL']
    buoy_id = config['buoy']
    atmo_source = config['atmo']

    self.update_state(state='INPROGRESS', meta={'message':'Downloading Landsat Data', 'config': config})
    metadata = buoycalib.landsat.download_amazons3(scene_id, bands)

    self.update_state(state='INPROGRESS', meta={'message':'Downloading Buoy Data', 'config': config})
    buoy_info = buoycalib.buoy.calculate_buoy_information(metadata, buoy_id)

    self.update_state(state='INPROGRESS', meta={'message':'Downloading Atmopsheric Data', 'config': config})
    atmosphere, coordinates = buoycalib.atmo.process(atmo_source, metadata, buoy_info)

    self.update_state(state='INPROGRESS', meta={'message':'Running MODTRAN', 'config': config})
    modtran_out = buoycalib.modtran.process(atmosphere, buoy_info[1], buoy_info[2], metadata['date'], metadata['scene_dir'])

    self.update_state(state='INPROGRESS', meta={'message':'Processing Atmopsheric Data', 'config': config})
    mod_ltoa_spectral = buoycalib.radiance.calc_ltoa_spectral(modtran_out, buoy_info[5])

    if 'MTL' in bands: bands.remove('MTL')   # TODO fix stupid thing here

    radiance = []
    for b in bands:
        self.update_state(state='INPROGRESS', meta={'message':'Calculating Radiance Band: {0}'.format(b), 'config': config})
        mod_ltoa = buoycalib.radiance.calc_ltoa(modtran_out[2], mod_ltoa_spectral, buoycalib.settings.RSR_L8[b])
        img_ltoa = buoycalib.landsat.calc_ltoa(metadata, buoy_info[1], buoy_info[2], b)

        radiance.extend([mod_ltoa, img_ltoa])

    reports = {'radiance': radiance}
    self.update_state(state='DONE', meta={'message': 'Completed', 'config':config, 'return':reports})
