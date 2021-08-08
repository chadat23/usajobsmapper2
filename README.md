# usajobsmapper2

## Dev
for uncooperative windows dev environments, set env with:

```
if (-not (Test-Path env:FLASK_APP )) { $env:FLASK_APP  = 'usajobsmapper' }
if (-not (Test-Path env:FLASK_ENV )) { $env:FLASK_ENV  = 'development' }
```

## Production
