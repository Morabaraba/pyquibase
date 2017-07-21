# Pyquibase

Pyquibase is a Python wrapper for [liquibase](http://www.liquibase.org/). 
There are other liquibase wrapper for python but they all work with YAML file. Since I want to use xml file for liquibase, I built my own liquibase wrapper for python.
Athough I use Pyquibase with xml files only, it should also work with other file types.

## Installation

```python
pip install pyquibase
```

## Usage

Currently it supports Sqlite, MySql, and Postgresql 


### Update
##### sqlite

```python
from pyquibase.pyquibase import Pyquibase

if __name__ == '__main__':
    pyquibase = Pyquibase.sqlite('test.sqlite', 'db-changelog-1.xml')
    pyquibase.update()
```

##### MySQL

```python
from pyquibase.pyquibase import Pyquibase

if __name__ == '__main__':
    pyquibase = Pyquibase.mysql(
        host            = 'localhost',
        port            = 3306,
        db_name         = 'pyquibase',
        username        = 'root',
        password        = 'test',
        change_log_file = 'db-changelog-1.xml'
    )
    pyquibase.update()
```

##### Postgresql

```python
from pyquibase.pyquibase import Pyquibase

if __name__ == '__main__':
    pyquibase = Pyquibase.postgresql(
        host            = 'localhost',
        port            = 3306,
        db_name         = 'pyquibase',
        username        = 'root',
        password        = 'test',
        change_log_file = 'db-changelog-1.xml'
    )
    pyquibase.update()
```

### Rollback
```python
pyquibase.rollback('tag')
```
