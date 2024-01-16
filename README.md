
# Reviewer Recommender

This project uses Python and argparse to run different algorithms on a specified GitHub project. The algorithms are `RevFinder`, `ChRev`, `TurnoverRec`, and `Sofia`.

## Prerequisites

You need to have Python and pip installed on your machine. You can download Python from [here](https://www.python.org/downloads/) and pip is included in Python 3.8 and later versions.

## Installation

1. Clone the [`Github-crawler`](https://github.com/Ehsan200/Github-crawler) repository to your local machine:

2. Navigate to the `Github-crawler` directory:

```bash
cd Github-crawler
```

3. Run the crawler commands to fetch the data (see help and usage in the [Github-crawler](https://github.com/Ehsan200/Github-crawler)):

4. Once the data has been fetched, set the `DATA_BASE_DIR` environment variable to the path of the `crawled-data` directory in the `Github-crawler` repository.

```bash
export DATA_BASE_DIR=<path-to-Github-crawler>/crawled-data
```

5. Navigate back to the parent directory and clone this repository to your local machine:

6. Navigate to the project directory:

```bash
cd reviewer-recommender
```

7. Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage

To run an algorithm on a GitHub project, use the following command:

```bash
python manager.py --r_owner <owner> --r_name <repo> <algorithm>
```

Replace `<owner>` with the GitHub project owner's username, `<repo>` with the name of the repository, and `<algorithm>` with the name of the algorithm you want to run. The available algorithms are `revFinder`, `chRev`, `turnoverRec`, and `sofia`.

If you want to run the project without using cache, add the `--no-cache` argument:

```bash
python manager.py --r_owner <owner> --r_name <repo> <algorithm> --no-cache
```

## Data Storage

The data fetched by the `Github-crawler` is stored in the `crawled-data` directory. This directory is located in the root of the `Github-crawler` repository. The data is organized by GitHub project, with each project having its own subdirectory.

The `DATA_BASE_DIR` environment variable should be set to the path of the `crawled-data` directory. This allows the algorithms in this project to access the fetched data.

[//]: # (todo: add more info about the data storage and algorithms results)

## Authors

- [Ehsan Movaffagh](https://github.com/Ehsan200)
- [Seyyed Alireza Ghazanfari](https://github.com/seyyedAlirezaGhazanfari)