# PrefLib-Jekyll

This repository contains the Jekyll project for the website [PrefLib.org](https://preflib.org).
The Jekyll project generates static files that are then hosted on GitHub pages. This is
the third implementation of PrefLib, after the initial static website and the 
[PrefLib-Django](https://github.com/PrefLib/PrefLib-Django) project. With this third implementation,
we are returning to a simple static site. The motivation stems from the following observations:

- Finding hosting for a Django project can be challenging and costly;
- Maintaining a static website is simpler and increases its likelihood of long-term survival;
- Full integration as a GitHub workflow allows for better community participation and reduce the load on ''official maintainers''.

Keeping these principles in mind when further developing the website will help ensure its long-term success.

In the following, we present some tips for maintainers and developers of [PrefLib.org](https://preflib.org).

## How to

- [Deploy to the GitHub pages](#deploy-to-the-github-pages)
- [Add/Modify a dataset or a datafile](#addmodify-a-dataset-or-a-datafile)
- [Update the list of papers citing PrefLib](#update-the-list-of-papers-citing-preflib)

### Deploy to the GitHub Pages

Manual deployment is usually unnecessary as each push to the repository triggers automatic deployment via the
[Build Jekyll and Deploy Pages](https://github.com/PrefLib/PrefLib-Jekyll/blob/main/.github/workflows/build_jekyll.yml)
action. If you want to manually run the action, you can do so on the
[action page](https://github.com/PrefLib/PrefLib-Jekyll/actions/workflows/build_jekyll.yml).

Note that the project uses custom Jekyll plugins which means that the default GitHub action 
to deploy Jekyll project cannot be used.

### Add/Modify a dataset or a datafile

The project works hand in hand with the [PrefLib-Data repository](https://github.com/PrefLib/PrefLib-Data).
To update the datasets and datafiles of the website, use the following steps:

1. Make the desired changes to the [PrefLib-Data repository](https://github.com/PrefLib/PrefLib-Data);
2. Use the provided script in the [PrefLib-Data repository](https://github.com/PrefLib/PrefLib-Data) to zip the datasets;
3. Import the updated datasets using the generated zip files and the script [import_dataset.py](https://github.com/PrefLib/PrefLib-Jekyll/blob/main/scripts/import_dataset.py) that you can find under `scripts/import_dataset.py`
4. Wait for the script to finish and re-build the website.

The script will automatically read the zipped datasets, extract the necessary information and update
the [dataset.yml](https://github.com/PrefLib/PrefLib-Jekyll/blob/main/preflib/_data/datasets.yml) and
[datafiles.yml](https://github.com/PrefLib/PrefLib-Jekyll/blob/main/preflib/_data/datafiles.yml) files
that are used when building the site.

The tags for the datasets are added on the [PrefLib-Data](https://github.com/PrefLib/PrefLib-Data)
side, but their description is given in the 
[dataset_tags.yml](https://github.com/PrefLib/PrefLib-Jekyll/blob/main/preflib/_data/dataset_tags.yml)
file. Modify them there if needed.

### Update the list of papers citing PrefLib

To update the list of papers citing PrefLib, modify the 
[citing_papers.yml](https://github.com/PrefLib/PrefLib-Jekyll/blob/main/preflib/_data/citing_papers.yml)
file, which is automatically read when the site is built.

## Development tips

### How to handle large zip files

Because of the limitations of GitHub, we cannot just upload all the zip files included in the Jekyll
projects (their size varies from 1MB to 600MB). To deal with that, the zip files are hosted as
assets of a release of the [PrefLib-Data repository](https://github.com/PrefLib/PrefLib-Data).
In this Jekyll project, we link directly to this repository for downloads, bypassing GitHub’s 
file-size restrictions while keeping the process fully integrated within the GitHub workflow

### Emulating dynamic websites via JavaScript

The website is fully static but offers functionalities of a dynamic website (the search page for instance).
This is possible because of our heavy use of JavaScript. While this approach may make the site somewhat
heavier and occasionally more challenging to maintain, it allows us to offer more functionalities.
