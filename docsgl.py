from lxml import  etree as et
from bs4 import BeautifulSoup
from pathlib import Path
import os

folder = 'gl3'


#collect all the  gl entries needed for current documentation

htdocs_dir = Path(os.getcwd(), 'htdocs')


project = et.Element('QtHelpProject')
project.set("version", '1.0')
namespace = et.SubElement(project, 'namespace')
namespace.text = 'gl.docs'
vf = et.SubElement(project, 'virtualFolder')
vf.text = 'htdocs'
cf = et.SubElement(project, 'customFilter')
cf.set('name', 'OpenGL 3')

cf_fa_opengl = et.SubElement(cf, 'filterAttribute')
cf_fa_opengl.text = 'opengl'
cf_fa_version = et.SubElement(cf, 'filterAttribute')
cf_fa_version.text = str(3)

fSection = et.SubElement(project, 'filterSection')
et.SubElement(fSection, 'filterAttribute').text = 'opengl'
et.SubElement(fSection, 'filterAttribute').text = '3'

toc = et.SubElement(fSection, 'toc')
section = et.SubElement(toc, 'section')
section.set('title', 'docs.GL')
section.set('ref', 'index.html')


def patch_html(file : Path, key = False):
    print("Patching file {0}".format(file))
    with open(str(file), mode='r') as source:
        soup = BeautifulSoup(source, 'html.parser')

    for link in soup.find_all('a'):
        if 'href' not in link.attrs:
            #print(link)
            continue

        if '.' in link.attrs['href'] or link.attrs['href'][-1] == '/':
            continue
        link.attrs['href'] += '.html'

    if (len(file.suffixes) and file.suffixes[-1] == '.html'):
        newFile = file
    else:
        newFile = Path(str(file) + ".html")

    with open(str(newFile), mode='w') as destination:
        destination.write(soup.prettify())

    if key:
        keywords = [x.text for x in soup.select('.fsfunc')] #css selector class fsfunc
        return keywords, newFile
    else:
        return newFile


keywords = et.SubElement(fSection, 'keywords')
gl_files = [gl_file for gl_file in htdocs_dir.glob('{0}/*'.format(folder))]
#list all gl files

for gl_file in gl_files:
    if len(gl_file.suffixes) == 0:
        keys, gl_file = patch_html(gl_file, True) #extract keys
        for key in keys:
            keyword = et.SubElement(keywords, 'keyword')
            keyword.set('name', key)
            keyword.set('id', 'gl::' + key)
            keyword.set('ref', str(gl_file.relative_to(htdocs_dir)))


files = et.SubElement(fSection, 'files')


def do_add_file(file : Path):
    if file.is_file():
        if len(file.suffixes) == 0:
            return
        else:
            elem = et.SubElement(files, 'file')
            elem.text = str(file.relative_to(htdocs_dir))
            if file.suffixes[-1] == '.html' and folder not in [x.name for x in file.parents]:
                patch_html(file)
    elif file.is_dir():
        for subfile in file.iterdir():
            do_add_file(subfile)




#list root html & js files
for file in htdocs_dir.iterdir():
    if (file.is_dir() and file.name.startswith('jquery')) or (file.is_dir() and file.name == folder) \
            or len(file.suffixes) > 0 and file.suffixes[-1] in ['.html', '.css', '.js']:
        do_add_file(file)



tree = et.ElementTree(project)
tree.write(str(htdocs_dir / "docsgl.qhp"), encoding='UTF-8', xml_declaration=True, pretty_print=True)