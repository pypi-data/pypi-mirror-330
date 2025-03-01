# sqlmodelgen

`sqlmodelgen` is a library to convert `CREATE TABLE` statements from SQL to classes inheriting `SQLModel` from the famous [sqlmodel library](https://sqlmodel.tiangolo.com/).

## Example

```python
from sqlmodelgen import gen_code_from_sql

sql_code = '''
CREATE TABLE Hero (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	secret_name VARCHAR NOT NULL, 
	age INTEGER, 
	PRIMARY KEY (id)
);

print(gen_code_from_sql(sql_code))
'''
```

generates:

```python
from sqlmodel import SQLModel, Field

class Hero(SQLModel, table = True):
    __tablename__ = 'Hero'
    id: int = Field(primary_key=True)
    name: str
    secret_name: str
    age: int | None
```

## Internal functioning

The library relies on [sqloxide](https://github.com/wseaton/sqloxide) to parse SQL code, then generates sqlmodel classes accordingly

## Possible improvements

- Support for more SQL data types
- Possibility to acquire in input actual database connections (like Postgres) or files (SQLite) and generate sqlmodel code accordingly