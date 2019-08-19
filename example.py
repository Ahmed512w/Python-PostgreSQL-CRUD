#!/usr/bin/env python3
from crud import Crud


table = Crud(
    user = 'postgres',
    password = 'sql',
    host = '127.0.0.1',
    port = '5432',
    dbname = 'postgres',
    table = 'cities',
    primarykey = 'city'
)


table.connect()


table.insert(
    city = 'fayoum',
    address = 'south of cairo'
)


table.insert_many(
    columns = ('city', 'address'),
    rows = [
        ['matrooh', 'north'],
        ['luxor', 'south']
    ]
)


table.commit()


table.select_all()


table.select_all(
    primaryKey_value = 'luxor'
)


table.select(
    columns = ['address'],
    primaryKey_value = 'luxor'
)


table.select(
    columns = ['address']
)


table.update(
    column = 'address',
    column_value = '50 KM south of cairo',
    primaryKey_value = 'fayoum'
)


table.update_multiple_columns(
    columns = ['city', 'address'],
    columns_value = ['qena', 'upperEgypt'],
    primaryKey_value = 'luxor'
)


table.delete(
    primaryKey_value = 'matrooh'
)


table.select_all()


table.delete_all()


table.close('commit')

