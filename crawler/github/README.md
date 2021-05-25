# GitHub organisations, user and repo reference into CyCAT.org

## Usage

~~~
$ python3 github-importer.py --help
usage: github-importer.py [-h] [-o ORG] [-f] [-r REPO]

GitHub import for CyCAT

optional arguments:
  -h, --help            show this help message and exit
  -o ORG, --org ORG     GitHub organisation (fallback to user if not existing
                        as org) to import
  -f, --full            Import all repositories as project in CyCAT
  -r REPO, --repo REPO  Limit to a single GitHub repository import
~~~

