# OSM Map Merger

> **IMPORTANT NOTE** This repository is part of the _Behavior-Semantic Scenery Description (BSSD)_ framework. Check out our BSSD documentation and overview repository in your git of choice:
[![GitLab](https://img.shields.io/badge/GitLab-330F63?style=flat&logo=gitlab&logoColor=white)](https://gitlab.com/tuda-fzd/scenery-representations-and-maps/behavior-semantic-scenery-description)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/TUDa-FZD/Behavior-Semantic-Scenery-Description)

This tool can be used to handle one or more maps in OSM-format such as [Lanelet2 maps](https://github.com/fzi-forschungszentrum-informatik/Lanelet2) including the BSSD extension.

**Features:**
- Assign positive IDs to all elements and add a "version" attribute if missing. This is necessary after modification or creation of OSM-maps (e.g. with [JOSM](https://josm.openstreetmap.de/)) without synchronizing with the OSM database.
- Remap single negative IDs without changing the positive IDs.
- Merge multiple OSM input files into a single OSM output file. This works also for a mixture of positive and negative IDs.
- Elements with "action"="delete" will be ignored.

Use the ```--help``` command for more information about the [usage](#usage).

## Requirements
+ Python 3.8 or higher
+ osmium >=3.2.0
+ lxml,
+ beautifulsoup4,
+ click

## Installation
### Using pip
```bash
pip install osm-map-merger
```
This will install the latest version of the OSM Map Merger available in [PyPI](https://pypi.org/project/osm-map-merger/) to your environment.

### Manual Installation

Clone the source code to a directory of your choice (```path/to/osm-map-merger-src/```).

If you are using virtual environments, make sure to activate the correct environment to install the library into e.g:

```bash
source /<path-to-my-project>/.venv/bin/activate
```

Install the library:
```bash
pip install -e path/to/osm-map-merger-src/
```

## Usage
To see a list of available commands use:  

```bash
osm-map-merger --help
```
