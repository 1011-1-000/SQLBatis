from tests.basic_test import db
from sqlbatis.transaction_manager import TransactionManager

tm = TransactionManager(db)

CREATE = 'INSERT INTO user(name) VALUES (:name)'
SELECT = 'SELECT * FROM user'
DELETE = 'DELETE FROM user WHERE id = 1'
UPDATE = 'UPDATE user SET name = :name WHERE id = 1'
COUNT = 'SELECT count(*) FROM user'


@db.query(CREATE)
def create(user):
    pass


@db.query(SELECT, fetch_all=True)
def select():
    pass


@db.query(UPDATE)
def update(name):
    pass


@db.query(DELETE)
def delete():
    pass


@db.query(COUNT, fetch_all=True)
def count():
    pass


@db.bulk_query(CREATE)
def bulk_create(users):
    pass


user = {
    'name': 'leo1'
}

users = [{
    'name': 'leo2'
}, {
    'name': 'leo3'
}]


@tm.transactional()
def transaction_test():
    create(user)
    raise Exception('transaction error')
    create(user)


@tm.transactional()
def transaction_outer():
    create(user)
    create(user)
    transaction_inner()


@tm.transactional()
def transaction_inner():
    create(user)
    raise Exception('transaction error')
