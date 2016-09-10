import collections
from tabulate import tabulate
from unidecode import unidecode
from bs4 import BeautifulSoup
import urllib
import time
import json

with open('joblist.list', 'r') as fin:
	all_lines = fin.readlines()

def makelist(table):
  	result = []
  	allrows = table.findAll('tr')
  	for row in allrows:
    		result.append([])
    		allcols = row.findAll('td')
    		for col in allcols:
      			thestrings = [unicode(s) for s in col.findAll(text=True)]
      			thetext = ''.join(thestrings)
      			result[-1].append(thetext)
  	return result

def getinfo(url):
	job_info = {}
	r = urllib.urlopen(url).read()
	soup = BeautifulSoup(r, 'html.parser')
	
	#JOB INFO
	topsection = soup.find('div', { "id" : "content-area" })
	metainfo = topsection.find('div', { "class" : "meta" })
	try:
		meta_tags = metainfo.findAll('div')
		meta_tags = [unidecode(x.text.strip()) for x in meta_tags][0].split('\n')
		job_info['Tags'] = meta_tags
		#print '{:20s} : {}'.format('Tags', ' | '.join(meta_tags))
	except: 
		job_info['Tags'] = []

	info = topsection.find('div', { "class" : "content" })
	try:
		infolist = info.findAll('div', { "class" : "field-item odd" })
		
		for item in infolist:
			field = dict(item.parent.parent.attrs).get('class', '')[-1].split('-')[2]
			try:
				label = unidecode(item.find('div', {"class" : "field-label-inline-first"}).text.strip()[:-1])
				if label == 'Web site':
					job_info[label] = item.find('a')['href']
					#print '{:20s} : {}'.format(label,item.find('a')['href'])
				elif label == 'Organisation':
					job_info['VBMlink'] = item.find('a')['href']
					#print '{:20s} : {}'.format(label,item.find('a')['href'])
					job_info[label] = unidecode(item.find('a').text)
					#print '{:20s} : {}'.format(label,unidecode(item.find('a').text))
				else:
					job_info[label] = unidecode(item.contents[2].strip())
					#print '{:20s} : {}'.format(label,unidecode(item.contents[2].strip()))
			except AttributeError:
				field = field.title()
				if field == 'Schedule':
					#print field
					z = makelist(item)
					z = [[unidecode(x) for x in y] for y in z]
					#print tabulate(z[1:], z[0])
					job_info[field] = z

				else:
					job_info[field] = unidecode(item.text.strip())
					#print '{:20s} : {}'.format(field,unidecode(item.text.strip()))
	except AttributeError:
		pass

	return job_info




with open('jobinfo.json', 'w') as fout:
	for line in all_lines:
		time.sleep(2)
		print line
		z = getinfo(line)
		if z:
			json.dump(z, fout)
			fout.write('\n')
