## Virtual Env

```
(.venv) deactivate
```

## Install

```
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
flask db init
flask db migrate -m "Initial migration."
python app.py

```
