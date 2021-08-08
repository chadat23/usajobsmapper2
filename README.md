# usajobsmapper2

## Dev
for uncooperative windows dev environments, set env with:

```
if (-not (Test-Path env:FLASK_APP )) { $env:FLASK_APP  = 'usajobsmapper' }
if (-not (Test-Path env:FLASK_ENV )) { $env:FLASK_ENV  = 'development' }
```

To set up dev environment:

```
python setup.py test
```

Many examples and info is at: https://flask.palletsprojects.com/en/2.0.x/tutorial/

Build a wheel:

```
python setup.py bdist_wheel
```



## Production

For production rename

```
.\venv\Lib\site-packages\usajobsmapper\example_config.cfg
```
to
```
.\venv\Lib\site-packages\usajobsmapper\config.cfg
```
and change the values within.
