import pyodbc

server = 'SCRATSERVER'
database = 'test'
username = 'scrat'
password = 'vitkovice'

# Vytvoření připojení
conn_str = (
    f'DRIVER={{SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
)
try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()


    sql_select = "SELECT * FROM clovek"
    cursor.execute(sql_select)
    rows = cursor.fetchall()

    for row in rows:
        print(', '.join(str(value) for value in row))

    sql_count = "SELECT COUNT(*) FROM clovek"
    cursor.execute(sql_count)
    count = cursor.fetchone()[0]
    print(f'Počet záznamů: {count}')

except Exception as e:
    print("Chyba při připojení nebo získání dat:", e)
finally:
    cursor.close()
    conn.close()
