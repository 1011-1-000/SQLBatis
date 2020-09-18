from tests.basic_test import db


CREATE = 'INSERT INTO user(name) VALUES (:name)'
SELECT = 'SELECT * FROM user'
DELETE = 'DELETE FROM user WHERE id = 1'
UPDATE = 'UPDATE user SET name = :name WHERE id = 1'
COUNT = 'SELECT count(*) FROM user'
SELECT_USER_BY_NAME = 'SELECT * FROM user WHERE name = :name'


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

extra_user = {
    'name': 'libra'
}

users = [{
    'name': 'leo2'
}, {
    'name': 'leo3'
}]

users_for_paged = [user for i in range(35)]
