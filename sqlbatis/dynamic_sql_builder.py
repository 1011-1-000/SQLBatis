from sqlalchemy.sql import and_, or_, text
from .errors import NotSupportedException


class DynamicSQLBuilder:

    def __init__(self, sql, dynamic_query_clauses):
        self.sql = sql
        self.dynamic_query_clauses = dynamic_query_clauses

    def dynamic_build(self, keys=[], default='and'):
        texts = []

        for key in keys:
            if key in self.dynamic_query_clauses:
                texts.append(text(self.dynamic_query_clauses[key]))
            else:
                raise KeyError(f'Error to build dynamic sql for the {key}')

        if texts:
            if default == 'and':
                return f'{text(self.sql)} WHERE {and_(*texts)}'
            elif default == 'or':
                return f'{text(self.sql)} WHERE {or_(*texts)}'
            else:
                raise NotSupportedException(
                    'Default behavior is not supported')
        else:
            return self.sql
