# learning-backend

### Creation of the virtual environment
> This step is not completely necessary (but yes recommended), use it to you preference. If you use Windows, call `python` instead of `python3`.
```
python3 -m venv .venv
```

If you made the venv in the previous step, run the following to activate it, `./.venv/bin/activate` (on Linux).

### Install dependencies
```
pip install -r requirements.txt
```

### Building Database
This project needs a local database with a specific structure, to build the database, execute the following line (on Linux):
```
python3 ./database/build.py
```

### Run the project
```
python3 -m flask run
```
or run `start.sh` (`start.bat` in Windows) to start in development mode
