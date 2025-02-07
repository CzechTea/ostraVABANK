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

    sql_insert = """
    INSERT INTO clovek (jmeno, prijmeni) VALUES (?, ?)
    """
    data = ('Prokop', 'Dveře')

    cursor.execute(sql_insert, data)
    conn.commit()

    print("Záznam byl úspěšně vložen :).")
except Exception as e:
    print("Chyba:", e)
finally:
    cursor.close()
    conn.close()
