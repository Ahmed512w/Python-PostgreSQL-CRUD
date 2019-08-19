#!/usr/bin/env python3
import sys, psycopg2, psycopg2.sql as sql


class Crud:
    def __init__(self, user, password, host, port, dbname, table, primarykey):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.dbname = dbname
        self.table = table
        self.primarykey = primarykey
        


    def connect(self):
        try:
            connection = psycopg2.connect(
                user = self.user,
                password = self.password,
                host = self.host,
                port = self.port,
                dbname = self.dbname
            )
            cursor = connection.cursor()
            print(
                '------------------------------------------------------------'
                '\n-# PostgreSQL connection & transaction is ACTIVE\n'
                )
        except (Exception, psycopg2.Error) as error :
            print(error, error.pgcode, error.pgerror, sep = '\n')
            sys.exit()
        else:
            self._connection = connection
            self._cursor = cursor
            self._counter = 0


    def _check_connection(self):
        try:
            self._connection
        except AttributeError:
            print('ERROR: NOT Connected to Database')
            sys.exit()


    def _execute(self, query, Placeholder_value = None):
        self._check_connection()
        if Placeholder_value == None or None in Placeholder_value:
            self._cursor.execute(query)
            print( '-# ' + query.as_string(self._connection) + ';\n' )
        else:
            self._cursor.execute(query, Placeholder_value)
            print( '-# ' + query.as_string(self._connection) % Placeholder_value + ';\n' )

    
    def commit(self):
        self._check_connection()
        self._connection.commit()
        print('-# COMMIT '+ str(self._counter) +' changes\n')
        self._counter = 0


    def close(self, commit = False):
        self._check_connection()
        if commit:
            self.commit()
        else:
            self._cursor.close()
            self._connection.close()
        if self._counter > 0:
            print(
                '-# '+ str(self._counter) +' changes NOT commited  CLOSE connection\n'
                '------------------------------------------------------------\n'
            )
        else:
            print(
                '-# CLOSE connection\n'
                '------------------------------------------------------------\n'
            )


    def insert(self, **column_value):
        insert_query  = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(self.table),
            sql.SQL(', ').join( map( sql.Identifier, column_value.keys() ) ),
            sql.SQL(', ').join(sql.Placeholder() * len(column_value.values()))
        )
        record_to_insert = tuple(column_value.values())
        self._execute(insert_query, record_to_insert )
        self._counter += 1


    def insert_many(self, columns, rows):
        insert_query  = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(self.table),
            sql.SQL(', ').join( map( sql.Identifier, columns ) ),
            sql.SQL(', ').join(sql.Placeholder() * len(rows[0]))
        )
        for row in rows:
            row = tuple(row)
            self._execute(insert_query, row )
            self._counter += 1


    def select(self, columns, primaryKey_value = None):
        if primaryKey_value == None:
            select_query = sql.SQL("SELECT {} FROM {}").format(
                sql.SQL(',').join(map(sql.Identifier, columns)),
                sql.Identifier(self.table)
            )
            self._execute( select_query )
        else:
            select_query = sql.SQL("SELECT {} FROM {} WHERE {} = {}").format(
                sql.SQL(',').join(map(sql.Identifier, columns)),
                sql.Identifier(self.table),
                sql.Identifier(self.primarykey),
                sql.Placeholder()
            )
            self._execute( select_query, ( primaryKey_value,))
        try:
            selected = self._cursor.fetchall()
        except psycopg2.ProgrammingError as error:
            selected = '# ERROR: ' + str(error)
        else:
            print('-# ' + str(selected) + '\n')
            return selected


    def select_all(self, primaryKey_value = None):
        if primaryKey_value == None:
            select_query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table))
            self._execute( select_query )
        else:
            select_query = sql.SQL("SELECT * FROM {} WHERE {} = {}").format(
                sql.Identifier(self.table),
                sql.Identifier(self.primarykey),
                sql.Placeholder()
            )
            self._execute( select_query, ( primaryKey_value,))
        try:
            selected = self._cursor.fetchall()
        except psycopg2.ProgrammingError as error:
            selected = '# ERROR: ' + str(error)
        else:
            print('-# ' + str(selected) + '\n')
            return selected


    def update(self, column, column_value, primaryKey_value):
        update_query  = sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}").format(
            sql.Identifier(self.table),
            sql.Identifier(column),
            sql.Placeholder(),
            sql.Identifier(self.primarykey),
            sql.Placeholder()
        )
        self._execute(update_query, ( column_value, primaryKey_value))
        self._counter += 1


    def update_multiple_columns(self, columns, columns_value, primaryKey_value):
        update_query  = sql.SQL("UPDATE {} SET ({}) = ({}) WHERE {} = {}").format(
            sql.Identifier(self.table),
            sql.SQL(',').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(sql.Placeholder() * len(columns_value)),
            sql.Identifier(self.primarykey),
            sql.Placeholder()
        )
        Placeholder_value = list(columns_value)
        Placeholder_value.append(primaryKey_value)
        Placeholder_value = tuple(Placeholder_value)
        self._execute(update_query, Placeholder_value)
        self._counter += 1


    def delete(self, primaryKey_value):
        delete_query  = sql.SQL("DELETE FROM {} WHERE {} = {}").format(
            sql.Identifier(self.table),
            sql.Identifier(self.primarykey),
            sql.Placeholder()
        )
        self._execute(delete_query, ( primaryKey_value,))
        self._counter += 1


    def delete_all(self):
        delete_query  = sql.SQL("DELETE FROM {}").format( sql.Identifier(self.table) )
        self._execute(delete_query)
        self._counter += 1

