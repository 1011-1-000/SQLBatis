## SQLBatis

![License](https://img.shields.io/github/license/1011-1-000/SQLBatis?style=flat-square)
![PyPI - Python Version](https://img.shields.io/badge/Python-3.6%20%7C%203.7%20%7C%203.8-blue?style=flat-square)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen?style=flat-square)
[![DOC](https://img.shields.io/badge/SQLBatis-doc-orange?style=flat-square)](https://sqlbatis.readthedocs.io/en/latest/index.html)

**Under Documentation**

SQLBatis is a tool that inspired by the Mybatis, it provides an easier way to interact with the database through the raw sql.

SQLBatis allows you to migrate, update your database according to the data model you defined in your app.Also, there are several decorators and builtin functions which give you capbility to interact with your database.

Let's try it.

### Requirements

-   [SQLAlchemy-Core](https://docs.sqlalchemy.org/en/13/core/tutorial.html)
-   [Alembic](https://alembic.sqlalchemy.org/)


### Installation
Install SQLBatis with command `pip`::

    pip install sqlbatis

### Quick Tutorial

Connect to the DB

```python
from sqlbatis import SQLBatis
db = SQLBatis('sqlite:///:memory:')
```

We have provided the decorator **@db.query** to execute the raw sql, Here are CRUD examples:

```python
from sqlalchemy import Column, Integer, String
from sqlbatis import SQLBatis, Model
db = SQLBatis('sqlite:///:memory:')

class User(Model):

    id = Column(Integer, primary_key=True)
    name = Column(String)
    full_name = Column(String)


@db.query('INSERT INTO user (name, full_name) VALUS(:name, :full_name)')
def create(name, full_name):
    pass

@db.query('SELECT * FROM user')
def query_user():
    pass

@db.query('UPDATE user SET name = :name WHERE id = :id')
def update_user(name, id):
    pass

@db.query('DELETE FROM user WHERE id = :id')
def delete_user(id):
    pass

if __name__ == '__main__':
    create('10111000', 'Leo')
```

### Documentation

[More details please refer to the docs](https://sqlbatis.readthedocs.io/en/latest/index.html)
