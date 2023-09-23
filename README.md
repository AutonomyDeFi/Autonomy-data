# Autonomy-data
Autonomy is an autonomous AI Agent and Data marketplace that allows users to buy, sell, and build composable AI systems.
# Running the backend
- Install Python version management tool: [pyenv](https://github.com/pyenv/pyenv) or [asdf](https://github.com/asdf-vm/asdf)
- Install `Python 3.9.14` using the Python version management tool and activate that version
- Install psycopg2
- Setup the backend, ensure you have python 3.9 or great installed
- Run the following steps:
  - run `pip install -e .` (Install the 'backend' package)
  - git submodule update --init --recursive to clone (or update) the subgraphs repo in backend/

