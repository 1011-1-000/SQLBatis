Execute the Query in a transaction
==================================
:meth:`sqlbatis.sqlbatis.transactional` is a decorator which help you to do the query in a transaction::

    @db.transactional()
    def query_in_transaction():
        create(user)
        raise Exception('transaction error')
        create(user)

Due to the exception raised in the function, the transaction will not be committed to the database, the first
create function will be rolled back.

In terms of the case below::

    @db.transactional()
    def transaction_outer_for_inner_exception():
        create(user)
        create(user)
        transaction_inner_for_inner_exception()


    @db.transactional()
    def transaction_inner_for_inner_exception():
        create(user)
        raise Exception('transaction error')

the error raised in the inner function, will cause the db operations roll back in the outer function. so nothing 
will be committed.


