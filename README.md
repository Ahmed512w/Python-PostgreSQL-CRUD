# Python PostgreSQL CRUD
Python PostgreSQL Insert, Select, Update and Delete table data to Perform CRUD Operations

# How to use
1. Install Psycopg2 on your machine to use PostgreSQL from Python by ```pip install psycopg2```.


2. Create instance from Crud Class and pass ( user, password, host, port, dbname, table, primarykey ):
````python
    # User – username you use to work with PostgreSQL, The default username for the PostgreSQL database is Postgres.
    # Password – Password is given by the user at the time of installing the PostgreSQL.
    # Host – host is the server name or Ip address on which PostgreSQL is running. if you are running on localhost, then you can use localhost, or it’s IP i.e., 127.0.0.0.
    # Port – The default port for the PostgreSQL database is 5432.
    # Database Name – Database name to which you want to connect. Here we are using Database named “postgres_db”.
    # Table – table to do CRUD Operations on it.
    # Primary Key – primay key of table.
    
    table = Crud(
        user = 'postgres',
        password = 'sql',
        host = '127.0.0.1',
        port = '5432',
        dbname = 'postgres',
        table = 'cities',
        primarykey = 'city'
    )
````
3. connect to Database and start sql transaction by ```.connect()``` method.
````python
    table.connect()
````


4. Crud class has a multiple methods used for crud operations
   - insert()
   - insert_many()
   - select()
   - select_all()
   - update()
   - update_multiple_columns()
   - delete()
   - delete_all()


5. To commit changes use ```.commit()``` method.
````python
     table.commit()
````



6. To end connection to Database use ```.close()``` method.
   - this method has an optional argument "commit" used to commit new changes
````python
     # close connection without commit chamges
     table.close()

     # commit changes and close connection
     table.close(True)
     # or: table.close("commit")
````


_________________________________________________________________________________________________________________________
#### How to use ````insert(**column_value)```` method.
   this method take keyword arguments ( name = value )
   - name is the column 
   - value is the value to be inserted
   ````python
       table.insert(
           city = 'fayoum',
           address = 'south of cairo'
       )
   ````


_________________________________________________________________________________________________________________________
#### How to use ```insert_many(columns, rows)``` method.
  - columns -must be list or tuple- columns to be inserted
  - rows -must be two dimensional list or two dimensional tuple- values to be inserted
   ````python
       table.insert_many(
           columns = ('city', 'address'),
           rows = [
                ['matrooh', 'north'],
                ['luxor', 'south']
           ]
        )
   ````


_________________________________________________________________________________________________________________________
#### How to use ```select_all([primaryKey_value])``` method.
this method has one optional argument ``` [primaryKey_value] ```
 - if primaryKey_value is present, the method returns row that has this primaryKey_value
 - if primaryKey_value is absent, the method returns all rows and columns
````python
     table.select_all()

     table.select_all(
         primaryKey_value = 'luxor'
     )
````

_________________________________________________________________________________________________________________________
#### How to use ```select(columns, primaryKey_value)``` method.
this method has two arguments ```columns, [primaryKey_value]```,primaryKey_value is optional argument
 - columns -must be a list or a tuple- you want to select
 - if primaryKey_value is present, the method returns row that has this primaryKey_value with selected columns
````python
    table.select(
        columns = ['address'],
        primaryKey_value = 'luxor'
    )

    table.select(
        columns = ['address']
    )
````

_________________________________________________________________________________________________________________________
#### How to use ```update(column, column_value, primaryKey_value)``` method.
  - column - column to be updated
  - column_value - the new value to be inserted
  - primaryKey_value - specify the row to be updated
````python
    table.update(
        column = 'address',
        column_value = '50 KM south of cairo',
        primaryKey_value = 'fayoum'
    )
````

_________________________________________________________________________________________________________________________
#### How to use ```update_multiple_columns(columns, columns_value, primaryKey_value)``` method.
 - columns -must be a list or tuple- columns to be updated
 - columns_value -must be a list or tuple- it is the new values to be inserted
 - primaryKey_value - specify the row to be updated
````python
    table.update_multiple_columns(
        columns = ['city', 'address'],
        columns_value = ['qena', 'upperEgypt'],
        primaryKey_value = 'luxor'
    )
````

_________________________________________________________________________________________________________________________
#### How to use ```delete(primaryKey_value)``` method.
 - primaryKey_value - specify the row to be deleted
````python
    table.delete(
        primaryKey_value = 'matrooh'
    )
````

_________________________________________________________________________________________________________________________
#### How to use ```delete_all()``` method.
 - delete all rows from the table
````python
    table.delete_all()
````

