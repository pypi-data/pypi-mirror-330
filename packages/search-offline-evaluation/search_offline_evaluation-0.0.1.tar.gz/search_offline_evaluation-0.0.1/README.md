# Search Offline Evaluation

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Search Extrinsic and Intrinsic Evaluation powered by LLMs

## Overview

This framework processes search logs together with ads information
and evaluates retrieval performance.

Offline evaluation is performed with two approaches:
- using intrinsic signals from search logs such as clicks and interactions.
- using LLMs to annotate each (query, ad) pair.

## Getting Started

### Prerequisites
- Python 3.10 or higher
- Git

### Environment Setup `.env`
To configure your development environment, you need to set up some variables in an `.env` file. Use the following [template](.env.template):

```
# GenAI key
OPENAI_API_KEY=...
BASE_URL="https://stg.genai.olx.io/" # use only if you want to use GenAI Platform API Key

```
**How to Obtain These Credentials**
Access [GenAI platform](https://stg.genai.olx.io/sso/key/generate) and request for a key for your project.
In DSEP Search team space, a specific key was created for the context of this project.

2. **Install Dependencies**: Navigate to the root directory of the project and run:
```bash
pipenv install --dev
```
OR 
```bash
make env-dev
```
to create .env locally

    - This command will create a virtual environment and install all dependencies listed in the Pipfile.

3. **Activate the Virtual Environment**: Before running any commands or Jupyter Notebooks, activate the virtual environment:
```bash
pipenv shell
```
4. **Run Jupyter Notebook or JupyterLab**:
    - `pipenv run python -m ipykernel install --user --name=<kernel-name>`: Installs the current pipenv environment as a Jupyter kernel. Replace <kernel-name> with a desired name for the kernel.
    - To launch Jupyter Notebook:

    ```bash
    pipenv run notebook
    ```

    - Or to launch JupyterLab:

    ```bash
    pipenv run lab
    ```
    - These commands will open Jupyter Notebook or JupyterLab in your default web browser with all dependencies loaded.

#### Commonly Used Commands:

- `pipenv sync`: Installs all dependencies listed in Pipfile.lock without modifying the lockfile.
- `pipenv shell`: Opens a new shell with the virtual environment activated. To exit this shell, use the exit command.
- `pipenv clean`: Removes unused packages from Pipfile.lock to maintain a minimal and clean environment.


### Before git commit and push

- apply notebook and code formatting:
    - `make format-apply`
- cleanup the sql queries with sqlformatter:
    - `make format-sql`

### Running the code

1. Start Mlflow Tracking Server
```bash
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --host 127.0.0.1 --port 8080
```

2. Run main.py
```bash
python main.py
```

### Additional Scripts

In addition to the main codebase we also have additional scripts in the `scripts` directory.

#### llm_relevance_judge.py

Script that reads all parquets within a specific directory and annotates all unique (query, ad) pairs with relevance judgements.

```
python scripts/llm_relevance_judge.py \
    --input filepath_to_input_parquets_directory \
    --output output_dir_save_output_parquets \
    --max-workers 4 \
    --max-requests 100
```

The input parquet files should follow the format:
- `id (int)` - a unique identifier for the sample
- `query (str)` - the textual search query
- `rankings (dict[str, list[dict]])` - results for a specific retrieval system
    - `key (str)`: retrieval system name (e.g. `vector_search`, `olx_search`)
    - `value (list[dict])`: the list of results (ads) that the retrieval system retrieved for the textual search query.
        - Each ad is a dict. **The dict needs to have at least an `id` and `title`**

#### evaluate.py

Scripts to generate evaluation metrics given 2 directories:
- `retrieval_dir`: Directory with parquets of retrieval results
- `judgements_dir`: Directory with parquets of judgements

The retrieval parquet files in `retrieval_dir` should follow the format:
- `id (int)` - a unique identifier for the sample
- `query (str)` - the textual search query
- `rankings (dict[str, list[dict]])` - results for a specific retrieval system
    - `key (str)`: retrieval system name (e.g. `vector_search`, `olx_search`)
    - `value (list[dict])`: the list of results (ads) that the retrieval system retrieved for the textual search query.
        - Each ad is a dict. **The dict needs to have at least an `id` and `title`**

The jugdgements parquet files in `judgements_dir` should follow the format (***this is the same format that is generated as output when running `llm_relevance_judge.py`***):
- `id (int)` - a unique identifier for the sample
- `query (str)` - the textual search query
- `judgements (dict[str, int)` - judgements for the ads
    - `key (str)`: id of an ad
    - `value (int)`: judgement score (binary or multi-degree)

```
python scripts/evaluate.py \
    --retrieval_dir directory_with_retrieval_results_parquet_files \
    --judgements_dir directory_with_judgements_parquet_files
```

## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         search_offline_evaluation and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── search_offline_evaluation   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes search_offline_evaluation a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

--------

