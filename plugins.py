import xml.etree.ElementTree as ET
from string import Template

NS = '{http://pkp.sfu.ca}'
root = ET.parse('plugins.xml').getroot()
s = Template('|$plugin|$name|$applications|$category|$summary|$homepage')
rows =[]

def ns(s):
    return ''.join([NS, s])

def header():
    rows.append('### OJS / OMP / OPS Plugins - list')

    rows.append('|Plugin|Name|OJS|OMP|OPS|category|Summary|Homepage')
    rows.append('|---|---|---|---|---|---|---|---|')

def plugins():
    for product in root:
        category = product.attrib.get('category')
        plugin = product.attrib.get('product')
        applications = [':x:', ':x:', ':x:']
        for metadata in product:
            if metadata.tag == ns('name'): name = metadata.text
            if metadata.tag == ns('homepage'): homepage = '[{}]({})'.format(name, metadata.text)
            if metadata.tag == ns('summary'):  summary = metadata.text

            if metadata.tag == ns('release'):
                for release in metadata:
                    if release.tag == ns('compatibility'):
                        for i, val in enumerate(['ojs2', 'omp', 'ops']):
                            if release.attrib.get('application') == val:
                                applications[i] = ':ok:'
        row = s.substitute(plugin=plugin, category=category, name=name, homepage=homepage,summary=summary,
                           applications='|'.join(applications))
        rows.append(row)

def main():
    header()
    plugins()
    file = open("README.md", "w")
    file.write('\n'.join(rows))
    file.close()

if __name__ == "__main__":
    main()

