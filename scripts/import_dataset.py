import csv
import os
import shutil
from zipfile import ZipFile

import yaml
from preflibtools.instances.dataset import read_info_file

if __name__ == "__main__":
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
            "zip_file_url": f"https://github.com/PrefLib/PrefLib-Data/releases/download/v1.0/{dataset_info['series']}_{dataset_info['abb']}.zip",
            "data_types": list(set(f["file_name"][-3:] for f in dataset_info["files"].values()))
        }
        with open(dataset_file_path, "a", encoding="utf-8") as dataset_file:
                yaml.dump([dataset_yml], dataset_file, default_flow_style=False, sort_keys=False, encoding='utf-8', allow_unicode=True)

        file_to_metadatas = dict()
        with open(os.path.join(tmp_dir_path, "metadata.csv"), encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=";")
            for row in reader:
                file_to_metadatas[row["file"]] = row

        datafile_yml = dict()
        for file_name, file_info in dataset_info["files"].items():
            print(f"\t{file_name}")
            if file_name[-3:] in ["toc", "toi", "soc", "soi", "cat", "wmd"]:
                metadata = file_to_metadatas[file_name]
            else:
                metadata = dict()

            try:
                num_voters = int(metadata["numVot"])
            except:
                num_voters = 0
            try:
                num_alternatives = int(metadata["numAlt"])
            except:
                num_alternatives = 0
            try:
                num_unique = int(metadata["numUniq"])
            except:
                num_unique = 0

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
                "num_unique_preferences": num_unique,
                "is_approval": metadata.get("isApproval", None) == "True",
                "is_strict": metadata.get("isStrict", None) == "True",
                "is_complete": metadata.get("isComplete", None) == "True",
                "is_single_peaked": metadata.get("isSP", None) == "True",
                "is_single_peaked_tree": metadata.get("isSPTree", None) == "True",
                "is_single_crossing": metadata.get("isSC", None) == "True",
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
