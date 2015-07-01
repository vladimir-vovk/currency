Simple currency conversion REST API with django rest framework.

# Installation

1. Install python3 and create virtualenv (optional).
2. Clone repo and cd to repo directory.
3. Install requirements:
```
pip install requirements/local.txt
```
4. Run app locally:
```
python3 currency/manage.py runserver
```

# Admin

Open [http://localhost:8000/admin](http://localhost:8000/admin) (user: admin, password: admin).

All available currencies for conversion are in "Currencies" table. You can manage them manually.

All currencies rates are in "Rates" table. To update rates use command:
```
python3 currency/manage.py update_rates.
```
You can run tests with:
```
python3 currency/manage.py test.
```

# REST API

### api/currency 
  Get all available currencies.
  
### api/currency/NAME
  Get details for currency with NAME.
  
### api/convert/AMOUNT/FROM_NAME/TO_NAME
  Get currency conversion result.
