Builtin Database Access Operations
==================================

The most common operations when we interact with a database are CRUD,
SQLBatis also provides these basic functions for your usage:

CRUD operations
---------------
- create: will create a row in the database, :meth:`sqlbatis.sqlbatis_dao.SQLBatisDao.create`  
- retrieve_by_id: will get a row according to the id which is also as required parameter need to pass to the function, :meth:`sqlbatis.sqlbatis_dao.SQLBatisDao.retrieve_by_id`: 
- retrieve_all: get all the rows in the table. :meth:`sqlbatis.sqlbatis_dao.SQLBatisDao.retrieve_all`
- update_by_id: Update the row in the database by the id and attrs. :meth:`sqlbatis.sqlbatis_dao.SQLBatisDao.update_by_id`
- delete_by_id: Delete the row by the primary key. :meth:`sqlbatis.sqlbatis_dao.SQLBatisDao.delete_by_id`
- filter_by: Filter the rows according to the dictionary we pass to the func. :meth:`sqlbatis.sqlbatis_dao.filter_by`


Bulk insert
-----------
- bulk_insert: provide a way to insert the multiple rows and update multiple rows in the database. :meth:`sqlbatis.sqlbatis_dao.SQLBatisDao.bulk_insert`