import glob
import os
import shutil
from bs4 import BeautifulSoup

files = glob.glob("./extracted/*/*xml")
print(len(files))

abstracts_2024 = []
for x in files:
    with open(x, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'xml')
        item = soup.find('publisher').text
        if item == "Digital Humanities Passau":
            abstracts_2024.append(x)

YEAR = "2024"
F_NAME = "abstract-{}-{}.xml"
for i, x in enumerate(abstracts_2024):
    cur_nr = f"{i:05}"
    new_name = F_NAME.format(YEAR, cur_nr)
    save_path = os.path.join("data", "editions", new_name)
    shutil.copy(x, save_path)
