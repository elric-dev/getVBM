import urllib
import time
import os

url = 'http://cabm.net/en/o/'
output = '/Users/hsalee/wechipin2/data/html/orgpage/'

input_file = '/Users/hsalee/wechipin2/data/lists/orglist.list'


def get_page(url_link, file_name):
    urllib.urlretrieve(url_link, file_name)
    return


with open(input_file, 'r') as fin:
    for line in fin:
        url = line
        org_id = url.split('/')[-1].strip()
        print org_id

        filename = os.path.join(output, org_id + '.html')

        get_page(url, filename)
        time.sleep(5)
