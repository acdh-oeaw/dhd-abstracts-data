import glob
import os
from bs4 import BeautifulSoup

from csae_pyutils import save_json

files = sorted(glob.glob("./extracted/*/*xml"))

lookup_dict = {}
for x in files:
    zenodo_id = os.path.split(x)[0].split("/")[-1]
    file_name = os.path.split(x)[-1]

    with open(x, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "xml")
    title = soup.find("title").text
    title = " ".join(title.split())
    lookup_dict[title] = zenodo_id
    lookup_dict[file_name] = zenodo_id

save_json(lookup_dict, "foo.json")


ids = {}
for x in sorted(glob.glob("./data/editions/*.xml")):
    with open(x, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "xml")
    file_name = os.path.split(x)[-1]
    title = soup.find("title").text
    root = soup.find_all()[0]
    xml_id = f"{root.get('xml:id')}.xml"
    title = " ".join(title.split())
    try:
        zenodo_id = lookup_dict[title]
    except KeyError:
        try:
            zenodo_id = lookup_dict[xml_id]
        except KeyError:
            continue
    ids[x] = zenodo_id
    pub_stmt = soup.find('publicationStmt')
    if pub_stmt:
        for idno in pub_stmt.find_all('idno', subtype="zenodo"):
            idno.decompose()
        idno = soup.new_tag('idno', type='url', subtype="zenodo")
        idno.string = f"https://zenodo.org/records/{zenodo_id}"
        pub_stmt.append(idno)
        with open(x, 'w', encoding='utf-8') as file:
            file.write(str(soup))

save_json(ids, "bar.json")
