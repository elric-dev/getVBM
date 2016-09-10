from bs4 import BeautifulSoup
import json
import os
from pprint import pprint

html_dir = '/Users/hsalee/wechipin2/data/html/orgpage/'
all_files = os.listdir(html_dir)


def fix_mail(email_str):
    email_str = email_str.replace("[dot]", ".")
    email_str = email_str.replace("[at]", "@")
    email_str = email_str.replace(" ", "")
    return email_str


def getinfo(file_path):
    org_info = {}
    soup = BeautifulSoup(open(file_path), 'html.parser')

    # ORG INFO
    org_info["Name"] = soup.find('h1', {"class": "title"}).text
    top_section = soup.find('div', {"id": "content-area"})
    org_info["Description"] = top_section.find('p').text
    info = top_section.find('div', {"class": "content"})
    infolist = info.findAll('div', {"class": "field-item odd"})

    for item in infolist:
        label = (item.find('div', {"class": "field-label-inline-first"}).text.strip()[:-1]).encode('UTF-8')
        if label == 'Web site':
            link = item.find('a')['href']
            org_info[label] = link.encode('UTF-8')
        elif label == 'Email address':
            link = item.find('span', {"class": "spamspan"}).text
            org_info[label] = fix_mail(link).encode('UTF-8')
        else:
            org_info[label] = (item.contents[2].strip())

    org_info['Jobs'] = []

    # ORG JOBS
    bottom_section = soup.find('div', {"class": "region region-content-bottom"})
    info = bottom_section.find('div', {"class": "view-content"})
    if info:
        infolist = info.findAll('li')
        for item in infolist:
            link = item.find('a')
            job_link = ('http://cabm.net' + link['href']).encode('UTF-8')
            org_info['Jobs'].append(job_link)
    return org_info


for item in all_files:
    file_path = os.path.join(html_dir, item)
    try:
        getinfo(file_path)
        #print '\n\n\n\n\n'
    except AttributeError, e:
        print item, e





'''
with open('orginfo.json', 'w') as fout:
    for line in all_lines:
        time.sleep(5)
        z = getinfo(line)
        json.dump(z, fout)
        fout.write('\n')
'''

# saving for later
'''
def getinfo(file_path):

    org_info = {}
    #jobj = json.loads(line)
    #name = jobj['name']

    #print name
    #org_info['Description'] = (jobj['description'])
    #vbm_url = jobj['vbm_link']
    #url = 'http://cabm.net' + vbm_url
    #org_info["VBM_link"] = (url)

    #r = urllib.urlopen(url).read()
    soup = BeautifulSoup(open(file_path), 'html.parser')

    # ORG INFO
    org_info["Name"] = soup.find('h1', {"class": "title"}).text
    topsection = soup.find('div', {"id": "content-area"})
    org_info["Description"] = topsection.find('p').text
    info = topsection.find('div', {"class": "content"})
    infolist = info.findAll('div', {"class": "field-item odd"})

    for item in infolist:
        label = (item.find('div', {"class": "field-label-inline-first"}).text.strip()[:-1]).encode('UTF-8')
        if label == 'Web site':
            link = item.find('a')['href']
            org_info[label] = link.encode('UTF-8')
        elif label == 'Email address':
            link = item.find('span', {"class": "spamspan"}).text
            org_info[label] = fixmail(link).encode('UTF-8')
        else:
            org_info[label] = (item.contents[2].strip())

    org_info['Jobs'] = []

    # ORG JOBS
    bottomsection = soup.find('div', {"class": "region region-content-bottom"})
    info = bottomsection.find('div', {"class": "view-content"})
    if info:
        infolist = info.findAll('li')

        for item in infolist:
            job_list = []
            link = item.find('a')
            #linkid = link.text
            #job_info['ID'] = linkid.split(')')[0][1:].encode('UTF-8')
            job_link = ('http://cabm.net' + link['href']).encode('UTF-8')
            #job_info['Schedule'] = item.find('span', {"class": "schedule_right"}).text.encode('UTF-8')
            #job_info['Description'] = (
            #    item.find('div', {"class": "views-field views-field-field-exigences-value"}).find('span', {
            #        "class": "field-content"}).contents[0])

            org_info['Jobs'].append(job_link)
    return org_info
'''
