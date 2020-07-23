import xml.etree.ElementTree as ET
from string import Template
import requests
import sys


NS = '{http://pkp.sfu.ca}'
PKP_SOFTWARE = ['ojs2', 'ops', 'omp']

def get_xml():
    r = requests.get('https://github.com/pkp/plugin-gallery/blob/master/plugins.xml')
    if r.status_code == 200:
        file = open("plugins.xml", "w")
        file.write(r.content.decode("utf-8"))
        file.close()
    else:
        sys.exit()



root = ET.parse('plugins.xml').getroot()
s = Template('|$plugin|$applications|$summary')
rows =[]

def ns(s):
    return ''.join([NS, s])

def header():
    rows.append('### OJS / OMP / OPS Plugins in Plugin Gallery')

    rows.append('|'.join(['Plugin','OJS','OPS','OMP','Summary']))
    rows.append('|---|---|---|---|---')

def run():
    plugins = {}
    for product in root:
        rank = 0
        category = product.attrib.get('category')
        p = product.attrib.get('product')
        plugins[p] = {}
        applications = ['-', '-', '-']
        software_present = [{i:False} for i in PKP_SOFTWARE]
        for metadata in product:
            if metadata.tag == ns('name'): name = metadata.text
            if metadata.tag == ns('homepage'): plugin = '[{}]({})'.format(name, metadata.text)
            if metadata.tag == ns('summary'):  summary = metadata.text

            if metadata.tag == ns('release'):
                for release in metadata:
                    if release.tag == ns('compatibility'):

                        for i, val in enumerate(PKP_SOFTWARE):
                            if release.attrib.get('application') == val:
                                if software_present[i][val] == False:
                                    rank += len(PKP_SOFTWARE) -i
                                software_present[i][val] = True
                                applications[i] = ':ok:'
        row = s.substitute(plugin=plugin,summary=summary,
                           applications='|'.join(applications))
        plugins[p]['row'] = row
        plugins[p]['rank'] = rank
    return  plugins

def main():
    get_xml()
    header()



    file = open("README.md", "w")
    file.write('\n'.join(rows))
    file.write('\n')
    items = run().items()
    for itm in sorted(items, key= lambda i:i[1]['rank'], reverse=True):
        file.write(itm[1].get('row'))
        print(itm[1].get('rank'))
        file.write('\n')


    file.close()

if __name__ == "__main__":
    main()

