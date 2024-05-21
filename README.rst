=====================
EuroCC Service Search
=====================


.. image:: https://img.shields.io/pypi/v/cc_service_search.svg
        :target: https://pypi.python.org/pypi/cc_service_search

.. image:: https://img.shields.io/travis/tfruboes/cc_service_search.svg
        :target: https://travis-ci.com/tfruboes/cc_service_search

.. image:: https://readthedocs.org/projects/cc-service-search/badge/?version=latest
        :target: https://cc-service-search.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




Simple service search for NCC Poland


* Free software: MIT license
* Documentation: https://cc-service-search.readthedocs.io.

Running with minikube
--------


Working with minikube registry
--------
Start your minikube cluster with
```
minikube start --driver=kvm --addons=registry,ingress
```

Check the registry is up using:

```
curl -I $(minikube ip):5000
```

Check the registry ip:

```
minikube ip
```


Then add `"insecure-registries" : [ "registry_ip:5000" ]` to `/etc/docker/daemon.json` (replace registry_ip with minikuobe ip).

In order to apply above option you need to restart docker deamon:


```
sudo systemctl daemon-reload; sudo systemctl restart docker
```

Note: above procedure needs to be repeated after minikube restarts, since ip address is likely to change.

Relase process
--------
Following instructions will build artifacts, including docker images. Currently they rely on minikubes' registry enabled.

1. Run `cc_service_search_frontend/build_and_deploy.sh`. This will build all frontend files and update them in cc_service_search/website_data/ 
   directory. Please note, that old files in this dir will be deleted
1. Change `appVersion` in helm chart to expected version after bump
1. Commit all changes
1. Bump version using:
   ```
   bumpversion patch # or minor or major
   ```
   this will update the package version and create a corresponding git tag
1. Run `make dist` to build python release files
1. Run `kubernetes/image/build.sh` to build and push docker images
   - note, that this automagically calls `make dist`
   - currently this pushes images to minikube image registry   

Running localy with minikube
-------

1. Go through steps described in "Release process" in order to build images (if no changes were made, only the last step is needed)
1. Deploy with
  ```
  cd kubernetes
  helm dep update helm
  helm dependency build helm
  helm install cc-service-search helm --create-namespace -n cc-service-search
  ```
1. Get service url with  `minikube service -n cc-service-search --url cc-service-search-cc-service-search`
1. Add ip from previous step to /etc/hosts with domain matching the one in helms' chart `values.yaml` file (by default - `ccsearch.com`)


Database initialization, data upload and managment
--------
Currently all database operations are performed using provided cli script `cc_service_search`. Scripts expects one of the following actions:

- `initdb` - initialize opensearch index
- `dropdb` - drop opensearch index 
- `upload` - upload data the index from xlsx file
- `compare` - compare exising data and candidate xlsx file (read only operation)

Script expects the following env variables to be set in the environment:

```
DB_HOST=  # for minikube deployments - obtain with `minikube ip`
DB_PORT=32123
DB_USER=admin
DB_PASSWORD= # must match value provided via admin_db_password variable in helms' chart values.yaml file
DB_INDEX=cc_service_database
```
Alternatively, you may create `.env` file with the following values set.


In order to initialize database run:

```
cc_service_search initdb
```

Next, upload data from xlsx file

```
cc_service_search upload --file <xlsx file path>
```




Localization support
--------

* i18next framework is used, with browserLanguageDetector (default settings, see https://github.com/i18next/i18next-browser-languageDetector)
  * Displayed language may be forced via query string parameter (http://localhost:3000/?lng=pl) or cookie (e.g. set cookie i18next=pl)
*  Place your translations inside `cc_search_frontend/public/locales directory`
* note, that opensearch queries rely on language detection performed by i18next/LangugeDetector - detected language value is used
  to filter documents. Please note it is not strictly necessary to have a translation avaliable (i.e. placed in directory above), 
* note - if language is not set by your website via cookie or url query string param, LangugeDetector will try different methods for language 
  determination, including browser language settings. In such case we may land with language set to unsopprted one. 
  
  In order to handle such situation search page will render in english (or with locale defined by FALLBACK_LOCALE env variable - 
  if visible within flask server env). All opensearch queries also use that language.



Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
