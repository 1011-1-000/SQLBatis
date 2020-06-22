Let's talk with DB in your app
==============================

Connect to the DB
-----------------
The first thing that we need to do is initialize the sqlbatis instance with DB url, so the tool can know
which database should be connected. The code snippet below::

    from sqlbatis import SQLBatis
    db = SQLBatis(sqlite:///:memory:)

To have a quick start, we use the sqlite as an example.

Actually the SQLBatis will pass all the parameters to the SQLAlchemy `create_engine <https://docs.sqlalchemy.org/en/13/core/engines.html#sqlalchemy.create_engine>`_ function, 
you can define the extra create options defined in the SQLAlchemy.

Execute the raw sql with @sqlbatis.query
----------------------------------------

Insert or update bulk records
-----------------------------

Paginate query with SQLBatis
----------------------------
