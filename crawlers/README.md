# ACS UPB Mobile crawlers

A collection of crawlers used by the app. These are for static websites (like the website that holds teacher information). These websites are updated less frequently, so it's fine if the scripts are run manually once in a while and the data is pushed to firebase.

## How to run

It's recommended to use [virtualenv](https://pypi.org/project/virtualenv/). If you have a virtualenv setup, skip this step.

```
virtualenv acs-upb-mobile-crawlers-env
```

Activate the virtual env ([more info](acs-upb-mobile-crawlers-env))

```
pip install -r requirements
python prof_info_scraper.py
```

## Requirements
Python 3.6+