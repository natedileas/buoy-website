import urllib
from app import celery

CHUNK = 1024 #* 1024 * 8

@celery.task(bind=True)
def background_task(self, auth=False):
    """
    needs source url (from webs ite) and destination save location


    """
    source_url = 'http://www.spitzer.caltech.edu/uploaded_files/images/0006/3034/ssc2008-11a12_Huge.jpg'
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}

    req = urllib.Request(source_url, headers=hdr)

    if auth:
        out_file = str(auth) + '.jpeg'
    else:
        out_file = 'test2.jpeg'

    try:
        opened = urllib.urlopen(req)
    except urllib.HTTPError as e:
        print(e)

    total_size = int(opened.info().getheader('Content-Length').strip())

    progress = 0
    self.update_state(state='PROGRESS')

    with open(out_file, 'wb') as f:
        while True:
            chunk = opened.read(CHUNK)
            if not chunk: break
            f.write(chunk)
            progress += CHUNK
            self.update_state(state='PROGRESS',
                meta={'current': progress, 'total': total_size, 'status': 'asdfghjk'})

    return {'current': total_size, 'total': total_size, 'status': 'Download completed!'}
