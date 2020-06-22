Let's talk with DB in your app
==============================

Connect to the DB
-----------------
The first thing that we need to do is initialize the sqlbatis instance with DB url, so the tool can know
which database should be connected. The code snippet below::

    from sqlbatis import SQLBatis
    db = SQLBatis('sqlite:///:memory:')

To have a quick start, we use the sqlite as an example.

Actually the SQLBatis will pass all the parameters to the SQLAlchemy `create_engine <https://docs.sqlalchemy.org/en/13/core/engines.html#sqlalchemy.create_engine>`_ function, 
you can define the extra create options defined in the SQLAlchemy.

Execute the raw sql with @db.query
----------------------------------------
`tips:` Explanation first, the db is the instance of SQLBatis, the same definition in the below sections

We have provided the decorator @db.query - :meth:`sqlbatis.sqlbatis.SQLBatis.query` to execute the raw sql, Hera are CRUD examples::

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


As you can see here, although it is named **query**, you still can execute the insert, update and delete statement. 
the parameters defined in the query is named style in the `Python DBAPI <https://www.python.org/dev/peps/pep-0249/>`_, 
you can pass the parameters to the function, and the decorator
will retrieve those values mapping with the parameters defined in the statement.

Also, you can use a dict instead of the positional arguments.::

    if __name__ == '__main__':
        dic = {
            'name': '10111000',
            'full_name': 'Leo'
        }
        create(dic)


The Results of the query is the RowSet object which defined in the SQLBatis, Please see the more details
in the API Reference - :class:`sqlbatis.row.RowSet`.

Insert or update bulk records
-----------------------------
In some scnarios, we need to do the bulk insert or update, actually, it is more efficient to do bulk operations
rather than do it one by one. This is a suitable work for the @db.bulk_query - :meth:`sqlbatis.sqlbatis.SQLBatis.bulk_query`::

    BULK_INSERT_SQL = 'INSERT INTO user (name, full_name) VALUS(:name, :full_name)'

    # users are the list of the user
    users = [{'name': '10111000', 'full_name': 'Leo'} for _ in range(16)]

    @db.bulk_query(BULK_INSERT_SQL)
    def bulk_insert(users):
        pass 

The main difference between the @db.query and @db.bulk_query, is the parameter that we pass to the function is the
list of dictionaries.


Paginate query with SQLBatis
----------------------------
@db.query_by_page - :meth:`sqlbatis.sqlbatis.SQLBatis.query_by_page` is a helper function 
to do the pagination. you can easier to do the paging query with this, the useage below::

    @db.query_by_page('SELECT * FROM user', page=1, page_size=10)
    def query_user_by_page():
        pass    

this decorator will recieve three parameters - sql, page, page_size. It is easy to understand what does it means.
will not explain it any more.

In terms of the wrong page or page size, the default process is:

    1. if the page size less than 1, will set the page size to 10
    2. if page less than 1, it means the 0 or negative page number, will set 1
    3. if page greater than max page, will set the page number to the max page number

The result of query_by_page is the :class:`sqlbatis.page_query_builder.PageResults`. Please get more details in API documentation.