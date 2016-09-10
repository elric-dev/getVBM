import re
import json
import sys
from pprint import pprint
from unidecode import unidecode

filename = '../data/orginfo.json'

def printit(jobj):
	for item in sorted(jobj.keys()):
		print '{:20s} : {}'.format(item, str(jobj[item]))
	print '='*150
	return

def modeller(line):
	jobj = json.loads(line)
	printit(jobj)
	return jobj

with open(filename) as fin:
	all_lines = fin.readlines()

with open('formatorgs.json', 'w') as fout:
        for line in all_lines:
                z = modeller(line)
		if z:
			json.dump(z, fout)
                	fout.write('\n')

