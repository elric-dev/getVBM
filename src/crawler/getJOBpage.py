import urllib
import time
import os


url = 'http://cabm.net/en/o/'
output = '/Users/hsalee/wechipin2/data/html/jobpage/'

inputfile = '/Users/hsalee/wechipin2/data/lists/joblist.list'

def getpage(url, filename):
    urllib.urlretrieve(url, filename)
    return


with open(inputfile, 'r' ) as fin:
    for line in fin:
        print line

        url = line.strip()

        job_id = line.split('/')[-1].strip()
        filename = os.path.join(output, job_id+'.html')

        getpage(url, filename)
        time.sleep(1)


