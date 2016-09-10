import re
import json
import sys
from pprint import pprint
from unidecode import unidecode

filename = '../data/jobinfo.json'

def printit(jobj):
	for item in sorted(jobj.keys()):
		print '{:20s} : {}'.format(item, str(jobj[item]))
	print '='*150
	return

def chkobj(jobj):
	if len(jobj.keys()) == 1:
		return False
	return True

def langreplace(langname):
	frlist = ['Allemand', 'Anglais', 'Arabe', 'Aucune langue de selectionnee', 'Autre', 'Bengali', 'Bilingue (F/A)', 'Chinois', 'Creole', 'Espagnol', 'Francais', 'Grec', 'Hebreu', 'Hindi/Ourdou', 'Italien', 'Polonais', 'Portugais', 'Roumain', 'Russe', 'Tagalog', 'Tamil', 'Vietnamien']
	enlist = ['German', 'English', 'Arab', None, 'Other', 'Bengali', 'Bilingual (F / E)', 'Chinese', 'Creole', 'Spanish', 'French', 'Greek', 'Hebrew', 'Hindi / Urdu', 'Italian', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Tagalog', 'Tamil', 'Vietnamese']
	idx = frlist.index(langname)
	return enlist[idx]

def contact(line):
	line = unidecode(line)
	if line.startswith('Please call the Volunteer Bureau of Montreal'): 
		#at 514.842.3351.  Please note the number of the request: 28852':
		return ['Volunteer Bureau of Montreal, request#:%s' %line.split(':')[-1], '514.842.3351', None]
	z = line.split('/')
	z = [x.strip() for x in z]
	name = z[0]
	if name == '':
		name = None
	pnum = z[1]
	if len(z) == 3:
		email = z[2]
	else:
		email = None
	return [name, pnum, email]

def desc(line):
	line = unidecode(line)
	z = line.split('|')
	z = [x.strip() for x in z]
	if z[0].startswith('Short-term') or z[0].startswith('One-time'):
		typ = z[0]
		z = z[1:]
	else:
		typ = 'Long-term'
	if z[0].startswith('The description of this request is only available in French.'):
		desc_en = None
	else:
		desc_en = z[0]
	z = z[1:]

	if z[0].startswith('Place of work'):
		desc_fr = None
		loc = z[0].split(':')[-1].strip()

	else:
		desc_fr = z[0]
		loc = z[1].split(':')[-1].strip()
	
	dates = re.findall(r'(\d+-\d+-\d+)', typ)
	if len(dates) == 2:
		date_start = dates[0]
		date_end = dates[1]
	elif len(dates) == 1:
		date_start = dates[0]
		date_end = dates[0]
	else:
		date_start = None
                date_end = None

	typ = typ.split()[0]
	
	return [loc, typ, desc_en, desc_fr, date_start, date_end]
	

def model_obj():
	model = {}
	model['Organization'] = None
	model['Causes'] = []
	model['Location'] = None
	model['Type'] = None
	model['Languages'] = []
	model['Title'] = None
	model['Description_en'] = None
	model['Description_fr'] = None
	model['Contact name'] = None
	model['Contact email'] = None
	model['Contact number'] = None
	model['Length of commitment'] = None
	model['Skills'] = []
	model['City'] = None
	model['Country'] = None
	model['Date_start'] = None
	model['Date_end'] = None
	return model

def modeller(line):
	model = {}
	jobj = json.loads(line)
	if chkobj(jobj):
		model['Organization'] = jobj['Organisation'] 
		try:
			model['Causes'] = unidecode(jobj['Causes']).split(' | ')
		except KeyError, e:
			pass

		model['Languages'] = [langreplace(x.strip().replace('"', '')) for x in unidecode(jobj['Language']).split('|')]
		model['Title'] = None
		
		model['Location'] = desc(jobj['Exigences'])[0]
		model['Type'] = desc(jobj['Exigences'])[1]
		model['Description_en'] = desc(jobj['Exigences'])[2]
		model['Description_fr'] = desc(jobj['Exigences'])[3]
		model['Date_start'] = desc(jobj['Exigences'])[4]
        	model['Date_end'] = desc(jobj['Exigences'])[5]
		model['Contact name'] = contact(jobj['Contact'])[0]
		model['Contact email'] = contact(jobj['Contact'])[2]
		model['Contact number'] = contact(jobj['Contact'])[1]
		try:
			model['Length of commitment'] = jobj['Length of commitment']
		except KeyError, e:
			pass
		
		model['Skills'] = unidecode(jobj['Activities']).split(' | ')
		model['City'] = 'Montreal'
		model['Country'] = 'Canada'
		
		#printit(model)
	return model

with open(filename) as fin:
	all_lines = fin.readlines()

with open('formatjobs.json', 'w') as fout:
        for line in all_lines:
                z = modeller(line)
		if z:
			json.dump(z, fout)
                	fout.write('\n')

