from bs4 import BeautifulSoup
import os

html_dir = '/Users/hsalee/wechipin2/data/html/orglist/'
output_dir = '/Users/hsalee/wechipin2/data/lists/'
all_files = os.listdir(html_dir)


def get_org_list(data_soup):
    section = data_soup.find('div', {"class": "item-list"})
    my_orgs = section.findAll("li")

    orgs = []
    for org_item in my_orgs:
        link = org_item.find('a')
        # desc = org_item.find('p')
        # org_dict = {'name': link.text, 'vbm_link': link['href'], 'description': desc.text}
        vbm_link = link['href'].split('/')[-1].strip()
        orgs.append(vbm_link)
    return orgs


all_orgs = []

for html_file in all_files:
    print html_file
    file_path = os.path.join(html_dir, html_file)
    soup = BeautifulSoup(open(file_path), "html.parser")
    org_list = get_org_list(soup)
    all_orgs.extend(org_list)

outfile = os.path.join(output_dir, 'orglist.list')
with open(outfile, 'w') as fout:
    for org in sorted(all_orgs, key=int):
        item = 'http://cabm.net/en/o/' + org
        fout.write('%s\n' % item)
