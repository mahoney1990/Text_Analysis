# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 11:39:17 2021

@author: mahon
"""

import sqlite3
from sqlite3 import Error
import pandas as pd

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = r"C:\Users\mahon\Documents\Python Scripts\pythonsqlite.db"

    sql_create_words_table = """ CREATE TABLE IF NOT EXISTS words (
                                        Speaker text,
                                        Date text ,
                                        Network text,
                                        Phrase text
                                    ); """

    sql_create_bigrams_table = """CREATE TABLE IF NOT EXISTS bigrams (
                                    Speaker text,
                                    Date text ,
                                    Network text,
                                    Phrase text
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_words_table)

        # create tasks table
        create_table(conn, sql_create_bigrams_table)
    else:
        print("Error! cannot create the database connection.")



main()



def create_words(conn,words):
    sql='''INSERT INTO words(Speaker,Date,Network,Phrase)
           VALUES(?,?,?,?)''' 
    
    curse=conn.cursor()
    curse.execute(sql,words)
    conn.commit()
    return curse.lastrowid

conn=create_connection(r"C:\Users\mahon\Documents\Python Scripts\pythonsqlite.db")
words=('Makkel','2021-1','WSU','This is a test')

create_words(conn, words)

wildcards = ','.join(['?'] * 4)

insert_sql = 'INSERT INTO words VALUES (%s)' % wildcards
conn.executemany(insert_sql, CNN_bigrams)

CNN_bigrams.to_sql('bigrams', conn, if_exists='append', index=False)
FOX_bigrams.to_sql('bigrams', conn, if_exists='append', index=False)

del CNN_bigrams
del FOX_bigrams

sql_query = pd.read_sql_query('''select*from bigrams ''',conn)












          
            
            
            
            
            
            
            