Simple currency conversion REST API with django rest framework.

# Installation

1. Install python3, then create virtualenv (optional).
2. Clone the repo, then cd to the repo directory.
3. Install requirements:
```
pip install requirements/local.txt
```
4. Run the app locally:
```
python3 currency/manage.py runserver
```

# Admin

Open [http://localhost:8000/admin](http://localhost:8000/admin) (user: admin, password: admin).

All available currencies for conversion are in the "Currencies" table. You can manually manage them.

All currencies rates are in the "Rates" table. To update rates use the following command:
```
python3 currency/manage.py update_rates.
```
You can run the tests as follows:
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
