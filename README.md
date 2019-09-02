# Crawline

Domain validator, parser and random dataset generator


File structure should be like:

    
    
    ---Services
            |
            ------Internal
                          |
                          ---------Validator
                          ---------Datasets
            ------External
                          |
                          ---------Frontend



Fork from awesome Slavko project.



## Requirements for usage (project global):

Python:
* jsonpickle
* mysql-connector-python


C++:
* https://github.com/lexborisov/myhtml/blob/master/INSTALL.md
* libmysqlclient-dev
* libcurl


Compilation flags: 
```
-lmysqlclient -lcurl
```
