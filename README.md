# dkb
Scrapes information from DKB bank account. Needs 2FA.

# Installation
Make sure you use a virtual env or similiar.
```sh
pip install dkb_robo
```

# Usage
```
>>> python3 src/main.py --help
usage: main.py [-h] [--secret_file SECRET_FILE] [--out_folder OUT_FOLDER]

optional arguments:
  -h, --help            show this help message and exit
  --secret_file SECRET_FILE
                        Path which stores the DKB credentials
  --out_folder OUT_FOLDER, -o OUT_FOLDER
                        Where to store the results
```

# Docker
You can also just run it via docker.

```sh
# Build
docker build -t dkb-account-info .

# Run
docker run --rm -v `pwd`:/usr/src/app/out -v `pwd`/.secrets:/usr/src/app/.secrets:ro -t dkb-account-info
```
