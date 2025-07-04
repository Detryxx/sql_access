import pyodbc
import sys
from typing import List, Tuple, Any

def connect_to_database():
    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=mate-test-sqlserver.database.windows.net;"
        "DATABASE=TopBike;"
        "UID=tanfolyam;"
        "PWD=vx#34T6k*E12;"
    )
    
    try:
        conn = pyodbc.connect(connection_string)
        print("Connection successful!")
        return conn
    except pyodbc.Error as e:
        print(f"Connection failed: {e}")
        return None

def get_table_names(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES;")
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return tables
    except pyodbc.Error as e:
        print(f"Error retrieving tables: {e}")
        return []

def format_results(cursor, results: List[Tuple]) -> None:
    if not results:
        print("No results to display.")
        return
    
    columns = [desc[0] for desc in cursor.description]
    column_widths = [len(col) for col in columns]
    
    for row in results:
        for i, value in enumerate(row):
            value_str = "NULL" if value is None else str(value)
            if len(value_str) > column_widths[i]:
                column_widths[i] = len(value_str)
    
    row_num_width = len(str(len(results)))
    
    print(" " * (row_num_width + 2), end="")
    for i, col in enumerate(columns):
        print(f"{col:<{column_widths[i] + 2}}", end="")
    print()
    
    for row_idx, row in enumerate(results):
        row_num = str(row_idx + 1)
        print(f"{row_num:<{row_num_width + 2}}", end="")
        
        for i, value in enumerate(row):
            value_str = "NULL" if value is None else str(value)
            print(f"{value_str:<{column_widths[i] + 2}}", end="")
        print()

def execute_sql_command(conn, sql_command: str) -> None:
    try:
        cursor = conn.cursor()
        cursor.execute(sql_command)
        
        if cursor.description:
            results = cursor.fetchall()
            print("Command executed successfully.")
            if results:
                format_results(cursor, results)
            else:
                print("Query executed successfully but returned no results.")
        else:
            conn.commit()
            print(f"Command executed successfully. Rows affected: {cursor.rowcount}")
        
        cursor.close()
        
    except pyodbc.Error as e:
        error_msg = str(e)
        if ']' in error_msg:
            error_msg = error_msg.split(']')[-1].strip()
        print(f"Error: {error_msg}")

def main():
    conn = connect_to_database()
    if not conn:
        return
    
    try:
        tables = get_table_names(conn)
        if tables:
            print(f"Tables: {', '.join(tables)}")
        else:
            print("No tables found or error retrieving tables.")
        
        while True:
            try:
                sql_command = input("Enter an SQL command (or type 'exit' to quit): ").strip()
                
                if sql_command.lower() == 'exit':
                    break
                
                if sql_command:
                    execute_sql_command(conn, sql_command)
                
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except EOFError:
                print("\nExiting...")
                break
    
    finally:
        conn.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()