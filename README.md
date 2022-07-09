# valorant-match-history

## Usage

### Nix & NixOS

```bash
# run the package from the repository
nix run .#

# build the package
nix build .#
```

### Linux & MacOS

```bash
# create virtual environment
python3 -m venv .venv

# use virtual environment
source .venv/bin/activate

# install dependencies from requirements.txt
pip3 install -r requirements.txt

# enable pre-commit
pre-commit install

# install package in development mode (changes will take effect automatically)
pip install -e .
```
