import psycopg2
from datetime import datetime as dt
from config import dbConfig

class Connection():
    
    def __init__(self):
        self.connection = None

    def connect(self, config):
        try:
            connection=psycopg2.connect(**config)
            print("Successfully connected to Postgres DB")
            self.connection = connection
        except Exception as exc:
            print("Error occured during connection "+type(exc).__name__+str(exc))

    def close(self):
        if self.connection:
            try:
                self.connection.close()
            except Exception:
                pass

    def execute_query(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            print(cursor.rowcount)
            resultset = cursor.fetchall()
            return resultset
        except Exception as exc:
            print(f"Exception occured of type {type(exc).__name__}, {str(exc)}")
    
    def get_column_list_and_datatype(self, schema_name, table_name):
        sql_statement = f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE UPPER(TABLE_SCHEMA) = '{schema_name.upper()}' AND upper(TABLE_NAME) = '{table_name.upper()}'"
        rs = self.execute_query(sql_statement)
        return rs

    def insert_data_to_table(self, schema_name, table_name, data_list):
        if len(data_list) <= 0:
            return "No data to insert"
        
        insert_value_list = []
        column_list_dt = self.get_column_list_and_datatype(schema_name=schema_name, table_name=table_name)
        column_list = [column[0].lower() for column in column_list_dt]

        for rec in data_list:
            value_list = self.get_values_from_list(rec, column_list)
            insert_value_list.append(value_list)

    def get_values_from_list(self, data_dict, column_list):
        data_dict_modified = {k.lower():v for k,v in data_dict.items()}
        values = []
        for column in column_list:
            value = data_dict_modified[column] if column in data_dict_modified else None
            values.append(value)
        return values

if __name__ == "__main__":
    conn = Connection()
    try:
        conn.connect(dbConfig)
        rs = conn.get_column_list_and_datatype("Public", "County_List")
        for column in rs:
            print(column[0])
        print(rs)
    except Exception as exc:
        print(str(exc))
    finally:
        conn.close()