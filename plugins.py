import xml.etree.ElementTree as ET
from string import Template
import requests
import sys
from collections import OrderedDict

NS = '{http://pkp.sfu.ca}'


def get_xml():
    r = requests.get('https://pkp.sfu.ca/ojs/xml/plugins.xml')
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
    rows.append('### OJS / OMP / OPS Plugins - list')

    rows.append('|Plugin|OJS|OMP|OPS|Summary')
    rows.append('|---|---|---|---|---')

def plugins():
    plugins = {}
    for product in root:
        rank = 0
        category = product.attrib.get('category')
        p = product.attrib.get('product')
        plugins[p] = {}
        applications = ['-', '-', '-']
        for metadata in product:
            if metadata.tag == ns('name'): name = metadata.text
            if metadata.tag == ns('homepage'): plugin = '[{}]({})'.format(name, metadata.text)
            if metadata.tag == ns('summary'):  summary = metadata.text

            if metadata.tag == ns('release'):
                for release in metadata:
                    if release.tag == ns('compatibility'):
                        for i, val in enumerate(['ojs2', 'omp', 'ops']):
                            if release.attrib.get('application') == val:
                                rank += 1
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
    for i in sorted(plugins().items()):
        file.write(i[1].get('row'))
        file.write('\n')


    file.close()

if __name__ == "__main__":
    main()

