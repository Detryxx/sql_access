import matplotlib.pyplot as plt
from math import inf
import pyodbc
from decimal import *
import datetime
 
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
 
def execute_sql_command(conn, sql_command: str) -> None:
        cursor = conn.cursor().execute(sql_command)
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        cursor.close()
        return results

def get_columns(col1 = "OrderDate" , col2 = "SubTotal"):
    conn = connect_to_database()
    if not conn:
        return

    sql_command = input("Enter an SQL command (or type 'exit' to quit): ").strip()
    db = execute_sql_command(conn, sql_command)
    wanted = []
    year = inf
    for i in range(len(db)):
        dbcol1 = db[i].get(col1)
        dbcol2 = db[i].get(col2)
        wanted.append([dbcol1.strftime('%Y-%m-%d'), str(dbcol2)])
        if int(dbcol1.strftime('%Y-%m-%d')[:4]) < year:
            year = int(dbcol1.strftime('%Y-%m-%d')[:4])

    totals = {}
    total = 0
    for y in range(4):
        for x in wanted:
            if int(x[0][:4]) == int(year):
                total += float(x[1])
        totals.update({year : total})
        year += 1
        total = 0
        

    conn.close()
    print("Connection closed.")
    return totals
 
 
plt.style.use('_mpl-gallery')
 
def graph(data: dict):
    fig, ax = plt.subplots(figsize=(10000000, 1000000))  # Adjust grid (figure) size
    fig.subplots_adjust(left=0.2, right=0.8, top=0.8, bottom=0.2)  # Add padding
 
    ax.plot(list(data.keys()), list(data.values()))
    print(list(data.keys()), list(data.values()))
 
    ax.set_ylabel('Sales')
    ax.set_xlabel('Time')
    plt.show()

if __name__ == "__main__":
    graph(get_columns())