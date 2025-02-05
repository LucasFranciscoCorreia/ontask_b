# -*- coding: utf-8 -*-

"""DB queries to manipulate columns."""

from typing import List

from django.db import connection
from psycopg2 import sql

from ontask import OnTaskDBIdentifier

sql_to_ontask_datatype_names = {
    # Translation between SQL data type names, and those handled in OnTask
    'text': 'string',
    'bigint': 'integer',
    'double precision': 'double',
    'boolean': 'boolean',
    'timestamp with time zone': 'datetime',
}

ontask_to_sql_datatype_names = {
    # Translation between OnTask data type names and SQL
    dval: key for key, dval in sql_to_ontask_datatype_names.items()
}


def add_column_to_db(
    table_name: str,
    col_name: str,
    col_type: str,
    initial=None,
):
    """Add an extra column of the given type with initial value.

    :param table_name: Table to consider

    :param col_name: Column name

    :param col_type: OnTask column type

    :param initial: initial value

    :return:
    """
    sql_type = ontask_to_sql_datatype_names[col_type]

    query_skel = 'ALTER TABLE {0} ADD COLUMN {1} ' + sql_type

    query = sql.SQL(query_skel).format(
        sql.Identifier(table_name),
        sql.Identifier(col_name),
        sql.Literal(initial),
    )

    if initial is not None:
        query = query + sql.SQL(' DEFAULT ') + sql.Literal(initial)

    connection.connection.cursor().execute(query)


def copy_column_in_db(
    table_name: str,
    col_from: str,
    col_to: str,
):
    """Copy the values in one column to another.

    :param table_name: Table to process

    :param col_from: Source column

    :param col_to: Destination column

    :return: Nothing. The change is performed in the DB
    """
    query = sql.SQL('UPDATE {0} SET {1}={2}').format(
        sql.Identifier(table_name),
        sql.Identifier(col_to),
        sql.Identifier(col_from),
    )

    connection.connection.cursor().execute(query)


def is_column_in_table(table_name: str, column_name: str) -> bool:
    """Check if a column is in the table.

    :param table_name: Table used for the check

    :param column_name: Column used for the check

    :return: Boolean
    """
    query = sql.SQL(
        'SELECT EXISTS (SELECT 1 FROM information_schema.columns '
        + 'WHERE table_name = {0} AND column_name = {1})',
    ).format(sql.Literal(table_name), sql.Literal(column_name))

    with connection.connection.cursor() as cursor:
        cursor.execute(query, [table_name, column_name])
        return cursor.fetchone()[0]


def is_column_unique(table_name: str, column_name: str) -> bool:
    """Return if a table column has all non-empty unique values.

    :param table_name: table

    :param column_name: column

    :return: Boolean (is unique)
    """
    query = sql.SQL('SELECT COUNT(DISTINCT {0}) = count(*) from {1}').format(
        OnTaskDBIdentifier(column_name),
        sql.Identifier(table_name),
    )

    # Get the result
    with connection.connection.cursor() as cursor:
        cursor.execute(query, [])
        return cursor.fetchone()[0]


def get_df_column_types(table_name: str) -> List[str]:
    """Get the list of data types in the given table.

    :param table_name: Table name

    :return: List of SQL types
    """
    with connection.connection.cursor() as cursor:
        cursor.execute(sql.SQL(
            'SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS '
            + 'WHERE TABLE_NAME = {0}').format(sql.Literal(table_name)))

        type_names = cursor.fetchall()

    return [sql_to_ontask_datatype_names[dtype[0]] for dtype in type_names]


def db_rename_column(table: str, old_name: str, new_name: str):
    """Rename a column in the database.

    :param table: table

    :param old_name: Old name of the column

    :param new_name: New name of the column

    :return: Nothing. Change reflected in the database table
    """
    with connection.connection.cursor() as cursor:
        cursor.execute(sql.SQL('ALTER TABLE {0} RENAME {1} TO {2}').format(
            sql.Identifier(table),
            sql.Identifier(old_name),
            sql.Identifier(new_name),
        ))


def df_drop_column(table_name: str, column_name: str):
    """Drop a column from the DB table storing a data frame.

    :param table_name: Table

    :param column_name: Column name

    :return: Drops the column from the corresponding DB table
    """
    with connection.connection.cursor() as cursor:
        cursor.execute(sql.SQL('ALTER TABLE {0} DROP COLUMN {1}').format(
            sql.Identifier(table_name),
            sql.Identifier(column_name)))


def get_text_column_hash(table_name: str, column_name: str) -> str:
    """Calculate and return the MD5 hash of a text column.

    :param table_name: table to use

    :param column_name: column to pull the values

    :return: MD5 hash of the concatenation of the column values
    """
    query = sql.SQL('SELECT MD5(STRING_AGG({0}, {1})) FROM {2}').format(
        OnTaskDBIdentifier(column_name),
        sql.Literal(''),
        sql.Identifier(table_name),
    )

    with connection.connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchone()[0]
