import os
from tqdm import tqdm
from sickle import Sickle
import requests
import zipfile
import glob
import shutil

YEAR = "2025"
F_NAME = "abstract-{}-{}.xml"
OAI_EP = "https://zenodo.org/oai2d"
OAI_SET = "user-dhd"
OAI_MD = "oai_dc"
FROM = "2025-02-02"
filters = {"metadataPrefix": OAI_MD, "from": FROM, "set": OAI_SET}
DL_URL = "https://zenodo.org/api/records/{}/files-archive"
zip_dir = "zip"
os.makedirs("zip", exist_ok=True)
sickle = Sickle(OAI_EP)


def save_response(response, filename):
    save_path = f"{os.path.join(zip_dir, filename)}.zip"
    with open(save_path, "wb") as f:
        f.write(response.content)


records = sickle.ListIdentifiers(**filters)

ids = set()
with open("ids.txt", "w") as f:
    for x in tqdm(records):
        record_id = x.identifier.split(":")[-1]
        ids.add(record_id)
        f.write(f"{record_id}\n")

zips = [os.path.split(x)[-1].replace(".zip", "") for x in glob.glob("zip/*.zip")]  # noqa:
len(zips)

for x in tqdm(ids):
    if x in zips:
        pass
    else:
        r = requests.get(DL_URL.format(x))
        save_response(r, x)


zip_files = glob.glob(os.path.join(zip_dir, "*.zip"))

extract_dir = "extracted"
os.makedirs(extract_dir, exist_ok=True)

for zip_path in tqdm(zip_files, desc="Extracting zip files"):
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            # Create a subdirectory for each zip file using its base name
            zip_basename = os.path.splitext(os.path.basename(zip_path))[0]
            extract_path = os.path.join(extract_dir, zip_basename)
            os.makedirs(extract_path, exist_ok=True)
            zip_ref.extractall(extract_path)
    except:  # noqa:
        print(zip_path)


teis = glob.glob("./extracted/*/*.xml")
for i, x in enumerate(teis):
    cur_nr = f"{i:05}"
    new_name = F_NAME.format(YEAR, cur_nr)
    save_path = os.path.join("data", "editions", new_name)
    shutil.copy(x, save_path)
