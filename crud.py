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
        


    def _connect(self):
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
                '\n------------------------------------------------------------'
                '\n-# PostgreSQL connection & transaction is ACTIVE'
                )
        except (Exception, psycopg2.Error) as error :
            print(error, error.pgcode, error.pgerror, sep = '\n')
            sys.exit()
        else:
            self._connection = connection
            self._cursor = cursor


    def _execute(self, query, Placeholder_value = None):
        if Placeholder_value == None or None in Placeholder_value:
            self._cursor.execute(query)
            print( '-# ' + query.as_string(self._connection) + ';' )
        else:
            self._cursor.execute(query, Placeholder_value)
            print( '-# ' + query.as_string(self._connection) % Placeholder_value + ';' )


    def _close(self):
        self._connection.commit()
        self._cursor.close()
        self._connection.close()
        print(
            '-# PostgreSQL transaction is committed & connection is closed\n'
            '------------------------------------------------------------\n'
        )


    def insert(self, **column_value):
        self._connect()
        insert_query  = sql.SQL("insert into {} ({}) values ({})").format(
            sql.Identifier(self.table),
            sql.SQL(', ').join( map( sql.Identifier, column_value.keys() ) ),
            sql.SQL(', ').join(sql.Placeholder() * len(column_value.values()))
        )
        record_to_insert = tuple(column_value.values())
        self._execute(insert_query, record_to_insert )
        self._close()


    def insert_many(self, columns, rows):
        self._connect()
        insert_query  = sql.SQL("insert into {} ({}) values ({})").format(
            sql.Identifier(self.table),
            sql.SQL(', ').join( map( sql.Identifier, columns ) ),
            sql.SQL(', ').join(sql.Placeholder() * len(rows[0]))
        )
        for row in rows:
            row = tuple(row)
            self._execute(insert_query, row )
        self._close()


    def select(self, columns, primaryKey_value = None):
        self._connect()
        if type(columns) == str and ( columns == '*' or columns.lower() == 'all' ):
            if primaryKey_value == None:
                select_query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table))  
            else:
                select_query = sql.SQL("SELECT * FROM {} where {} = {}").format(
                    sql.Identifier(self.table),
                    sql.Identifier(self.primarykey),
                    sql.Placeholder()
                )
        elif type(columns) == list or type(columns) == tuple:
            if primaryKey_value == None:
                select_query = sql.SQL("SELECT {} FROM {}").format(
                    sql.SQL(',').join(map(sql.Identifier, columns)),
                    sql.Identifier(self.table)
                )
            else:
                select_query = sql.SQL("SELECT {} FROM {} where {} = {}").format(
                    sql.SQL(',').join(map(sql.Identifier, columns)),
                    sql.Identifier(self.table),
                    sql.Identifier(self.primarykey),
                    sql.Placeholder()
                )
        try:
            self._execute( select_query, ( primaryKey_value,))
            selected = self._cursor.fetchall()
        except psycopg2.ProgrammingError as error:
            selected = '# ERROR: ' + str(error)
        print('-# selected >> '+ str(selected) )
        self._close()
        return selected


    def update(self, column, column_value, primaryKey_value):
        self._connect()
        update_query  = sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}").format(
            sql.Identifier(self.table),
            sql.Identifier(column),
            sql.Placeholder(),
            sql.Identifier(self.primarykey),
            sql.Placeholder()
        )
        self._execute(update_query, ( column_value, primaryKey_value))
        self._close()


    def update_multiple_columns(self, columns, columns_value, primaryKey_value):
        self._connect()
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
        self._close()


    def delete(self, primaryKey_value):
        self._connect()
        delete_query  = sql.SQL("DELETE FROM {} WHERE {} = {}").format(
            sql.Identifier(self.table),
            sql.Identifier(self.primarykey),
            sql.Placeholder()
        )
        self._execute(delete_query, ( primaryKey_value,))
        self._close()


    def delete_all(self):
        self._connect()
        delete_query  = sql.SQL("DELETE FROM {}").format( sql.Identifier(self.table) )
        self._execute(delete_query)
        self._close()

