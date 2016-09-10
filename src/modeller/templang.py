z = []

with open('lang', 'r') as fin:
	for line in fin:
		z.extend([x.strip().replace('"', '') for x in line.split('|')])

langs = sorted(list(set(z)))
for item in langs:
	print item
