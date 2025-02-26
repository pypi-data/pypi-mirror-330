import sqlite3
from typing import List,Tuple, Optional, Any, Union
class LTMSqlite:
    """SQLite database connection for long term memory."""
    def __init__(self,db_path:str):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
    def connect(self):
        "Intializes the connection and cursor objects based on the DB path."
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            print("Error connecting to the database: "+str(e))
    def __enter__(self):
        self.connect()
        return self
    def close(self):
        "Closes the sqlite connection and sets the connection and cursor values to None."
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
    def __exit__(self):
        self.close()
    def create_table(self,table_name: str,columns: List[str]):
        "Inputs a table name and a list of columns and creates the table in the sqlite database."
        column_str = ", ".join(columns)
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_str})"
        try:
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print(f"Table {table_name} created successfully!")
            print(self.get_columns(table_name))
        except Exception as e:
            print(f"Error in creating table {table_name}: "+str(e))    
    def get_columns(self, table_name: str):
        "Returns the list of columns in the particular table"
        pragma_query_str = f"PRAGMA table_info({table_name})"
        try:
            self.cursor.execute(pragma_query_str)
            columns = self.cursor.fetchall()
            column_names = [column[1] for column in columns]
            return column_names
        except Exception as e:
            print(f"Error getting table info for {table_name}: "+str(e))
            return False
    def insert(self,table_name: str, columns_and_values: List[Tuple]):
        "Inserts values into a table specified by their columns."
        columns = [t[0] for t in columns_and_values]
        values = [t[1] for t in columns_and_values]
        column_str = ", ".join(columns)
        values_str =  ", ".join(["?"] * len(values))
        insert_query_str = f"INSERT INTO {table_name} ({column_str})  VALUES ({values_str})"
        try:
            self.cursor.execute(insert_query_str,values)
            self.connection.commit()
        except Exception as e:
            print(f"Error inserting the values into the Table {table_name}: "+str(e))
    def select(self,table_name: str, columns: List[str] = None, where_condition: str = None, params: Optional[Tuple[Any, ...]] = None, distinct: bool = False):
        "Selects rows from a table. If no rows provided as an argument, then selects the whole table. Accepts optional WHERE conditions and parameters as well."
        try:
            if columns is not None:
                columns_str = " ,".join(columns)
                if distinct == True:
                    select_query_str = f"SELECT DISTINCT {columns_str} FROM {table_name}"
                else:
                    select_query_str = f"SELECT {columns_str} FROM {table_name}"
            else:
                if distinct == True:
                    select_query_str = f"SELECT DISTINCT * FROM {table_name}"
                else:
                    select_query_str = f"SELECT * FROM {table_name}"
            if where_condition is not None:
                select_query_str+= f" WHERE {where_condition}"
            if params is not None:
                self.cursor.execute(select_query_str,params)
            else: 
                self.cursor.execute(select_query_str)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving data from table {table_name}: "+str(e))
    def update(self, table_name: str, columns_and_values: List[Tuple], where_condition: str = None,params: Optional[Tuple[Any, ...]] = None):
        "Updates particular values in the columns provided the values and the WHERE condition."
        try:
            string_list = [f"{t[0]} = ?" for t in columns_and_values]  # Generates "column1 = ?, column2 = ?, ..."
            set_clause = ", ".join(string_list)
            update_query_str = f"UPDATE {table_name} SET {set_clause}"
            if where_condition:
                update_query_str += f" WHERE {where_condition}"
            update_values = [t[1] for t in columns_and_values]
            if params:
                update_values.extend(params)
            self.cursor.execute(update_query_str, update_values)
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating table '{table_name}': {e}")
            return False
    def delete(self, table_name: str, where_condition: str = None, params: Optional[Tuple[Any, ...]] = None):
        "Deletes data from a table given a WHERE condition and optional parameters. Deletes everything from the table if not WHERE condition is provided."
        if where_condition is None:
            delete_query_str = f"DELETE FROM {table_name}"
        else:
            delete_query_str = f"DELETE FROM {table_name} WHERE {where_condition}"
        try:
            if params is None:
                self.cursor.execute(delete_query_str)
            else:
                self.cursor.execute(delete_query_str,params)
            self.connection.commit()
            return self.cursor.rowcount
        except Exception as e:
            print(f"Error on DELETE operation on table {table_name}: "+str(e))
            return False
    def drop_table(self, table_name: str):
        "Drops the table from the database."
        drop_query_str = f"DROP TABLE {table_name}"
        try:
            self.cursor.execute(drop_query_str)
            self.connection.commit()
            print(f"Table {table_name} dropped successfully!")
        except Exception as e:
            print(f"Error dropping table {table_name}: "+str(e))