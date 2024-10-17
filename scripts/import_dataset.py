import os
import shutil
from zipfile import ZipFile

import yaml
from preflibtools.instances import get_parsed_instance
from preflibtools.instances.dataset import read_info_file
from preflibtools.properties.basic import is_approval

zip_files = sorted([os.path.join("zip", f) for f in os.listdir("zip") if f.endswith(".zip")])
# zip_files = ["zip/00001 - irish.zip", "zip/00002 - debian.zip", "zip/00003 - nasa.zip"]

dataset_file_path = os.path.join("..", "preflib", "_data", "datasets.yml")
datafile_file_path = os.path.join("..", "preflib", "_data", "datafiles.yml")

with open(dataset_file_path, "w", encoding="utf-8") as dataset_file:
    pass
with open(datafile_file_path, "w", encoding="utf-8") as datafile_file:
    pass

for zip_file in zip_files:
    print(f"Importing {zip_file}")
    tmp_dir_path = "tmp"
    os.makedirs(tmp_dir_path, exist_ok=True)

    with ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(tmp_dir_path)
    dataset_info = read_info_file(os.path.join(tmp_dir_path, "info.txt"))
    dataset_yml = {
        "name": dataset_info["name"],
        "abbreviation": dataset_info["abb"],
        "series_number": dataset_info["series"],
        "tags": dataset_info["tags"],
        "publication_date": dataset_info["publication_date"],
        "description": dataset_info["description"],
        "required_citations": dataset_info["citations"],
        "selected_studies": dataset_info["studies"],
        "num_files": len(dataset_info["files"]),
        "zip_file_size": os.path.getsize(zip_file),
        "zip_file_url": f"https://github.com/PrefLib/PrefLib-Data/raw/refs/heads/main/zip/dataset/{dataset_info['series']} - {dataset_info['abb']}.zip",
        "data_types": list(set(f["file_name"][-3:] for f in dataset_info["files"].values()))
    }
    with open(dataset_file_path, "a", encoding="utf-8") as dataset_file:
            yaml.dump([dataset_yml], dataset_file, default_flow_style=False, sort_keys=False, encoding='utf-8', allow_unicode=True)

    datafile_yml = dict()
    for file_name, file_info in dataset_info["files"].items():
        print(f"\t{file_name}")
        if file_name[-3:] in ["toc", "toi", "soc", "soi", "cat", "wmd"]:
            instance = get_parsed_instance(os.path.join(tmp_dir_path, file_name))
            num_voters = instance.num_voters
            num_alternatives = instance.num_alternatives
            approval_instance = is_approval(instance) if instance.data_type in ["toc", "soc", "toi", "soi",
                                                            "cat"] else None
        else:
            num_voters = 0
            num_alternatives = 0
            approval_instance = None
        datafile_yml[file_name] = {
            "name": file_name,
            "dataset": dataset_info["abb"],
            "data_type": file_name[-3:],
            "modification_type": file_info["modification_type"],
            "relates_to": file_info["relates_to"],
            "related_files": [],
            "title": file_info["title"],
            "description": file_info["description"],
            "publication_date": file_info["publication_date"],
            "size": os.path.getsize(os.path.join(tmp_dir_path, file_name)),
            "url": f"https://raw.githubusercontent.com/PrefLib/PrefLib-Data/main/datasets/{dataset_info['series']} - {dataset_info['abb']}/{file_name}",
            "num_voters": num_voters,
            "num_alternatives": num_alternatives,
            "is_approval": approval_instance,
            "is_single_peaked": None,
            "is_single_peaked_circle": None,
            "is_single_peaked_tree": None,
            "is_single_crossing": None,
            "is_1euclidean": None,
            "is_euclidean": None,
        }
    files_to_remove = []
    for file_name, file_dict in datafile_yml.items():
        if file_dict["relates_to"]:
            datafile_yml[file_dict["relates_to"]]["related_files"].append({
                "name": file_dict["name"],
                "description": file_dict["description"],
                "url": file_dict["url"],
                "size": file_dict["size"]
                })
            files_to_remove.append(file_name)
    for f in files_to_remove:
        del datafile_yml[f]

    with open(datafile_file_path, "a", encoding="utf-8") as datafile_file:
            yaml.dump(list(datafile_yml.values()), datafile_file, default_flow_style=False, sort_keys=False, encoding='utf-8', allow_unicode=True)

    shutil.rmtree(tmp_dir_path)
