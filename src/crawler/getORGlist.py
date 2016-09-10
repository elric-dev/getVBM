import urllib
import time
import os


url = 'http://cabm.net/en/o'
output = '../../data/html/orglist/'


def getpage(url, filename):
    urllib.urlretrieve(url, filename)
    return

url_i = url


for i in range(1, 11):
    print(url_i)
    filename = str(i)+'.html'
    filename = os.path.join(output, filename)
    getpage(url_i, filename)
    url_i = url + '?page=%s' % str(i)
    time.sleep(1)


