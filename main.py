import subprocess
import sys
import logging
import socket
import json

from threading import Thread

# Instalce chybějících balíčků, primarně pyodbc
required_packages = ["pyodbc"]
def install_missing_packages(packages):
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            print(f"{package} není nainstalován, instaluji...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_missing_packages(required_packages)

import pyodbc

# Konfigurace Loggování
logging.basicConfig(
    filename="bank_log.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Načtení databázeové konfigurace "config.json"
with open("config.json") as f:
    DB_CONFIG = json.load(f)

# Připojení k databázi
def get_db_connection():
    conn_str = f"DRIVER={{SQL Server}};SERVER={DB_CONFIG['SERVER']};DATABASE={DB_CONFIG['DATABASE']};UID={DB_CONFIG['USERNAME']};PWD={DB_CONFIG['PASSWORD']}"
    try:
        return pyodbc.connect(conn_str)
    except pyodbc.Error as e:
        logging.error(f"Chyba s připojením databáze: {e}")
        return None

# Server Config
HOST = "192.168.2.3"
PORT = 65432
TIMEOUT = 120

# SQL Query
def execute_query(query, params=(), fetch=False):
    conn = get_db_connection()
    if conn is None:
        return None
    cursor = conn.cursor()
    cursor.execute(query, params)
    if fetch:
        result = cursor.fetchall()
        conn.close()
        return result
    conn.commit()
    conn.close()

# Handlování příkazů od klienta
def handle_command(command, client_socket, client_ip):
    try:
        parts = command.strip().split()
        if not parts:
            response = "ER Neznámý příkaz."
        else:
            response = parts[0].upper()

        if response == "BC":
            ip = client_socket.getsockname()[0]
            response = f"BC {ip}"

        elif response == "AC":
            last_account = execute_query("SELECT MAX(account_number) FROM Accounts", fetch=True)
            account_number = (last_account[0][0] + 1) if last_account[0][0] else 10000
            execute_query("INSERT INTO Accounts (account_number, balance) VALUES (?, 0)", (account_number,))
            response = f"AC {account_number}/{HOST}"

        elif response == "AD" and len(parts) >= 3:
            account, amount = int(parts[1].split('/')[0]), int(parts[2])
            execute_query("UPDATE Accounts SET balance = balance + ? WHERE account_number = ?", (amount, account))
            response = "AD"

        elif response == "AW" and len(parts) >= 3:
            account, amount = int(parts[1].split('/')[0]), int(parts[2])
            balance = execute_query("SELECT balance FROM Accounts WHERE account_number = ?", (account,), fetch=True)
            if balance and balance[0][0] >= amount:
                execute_query("UPDATE Accounts SET balance = balance - ? WHERE account_number = ?", (amount, account))
                response = "AW"
            else:
                response = "ER Nedostatek prostředků nebo účet neexistuje."

        elif response == "AB" and len(parts) >= 2:
            account = int(parts[1].split('/')[0])
            balance = execute_query("SELECT balance FROM Accounts WHERE account_number = ?", (account,), fetch=True)
            response = f"AB {balance[0][0]}" if balance else "ER Účet neexistuje."

        elif response == "BA":
            total = execute_query("SELECT SUM(balance) FROM Accounts", fetch=True)
            response = f"BA {total[0][0] if total[0][0] else 0}"

        elif response == "BN":
            count = execute_query("SELECT COUNT(*) FROM Accounts", fetch=True)
            response = f"BN {count[0][0]}"

        else:
            response = "ER Neznámý příkaz."

    except Exception as e:
        response = "ER Neznámý příkaz."
        logging.error(f"Chyba: {str(e)}")

    client_socket.send(response.encode("utf-8"))
    logging.info(f"{client_ip} použil příkaz: {command.strip()} -> Odpověď zní: {response}")

# Proces klienta
def handle_client(client_socket, client_addr):
    try:
        client_socket.settimeout(TIMEOUT)
        while True:
            data = client_socket.recv(1024).decode("utf-8")
            print(data)
            if not data:
                break
            handle_command(data, client_socket, client_addr[0])
    except Exception as e:
        logging.warning(f"Chyba při komunikaci s klientem {client_addr[0]}: {str(e)}")
    finally:
        client_socket.close()
        print(f"Spojení s {client_addr[0]} ukončen." )

# Spuštění serveru
def start_server():
    logging.info("Spouští se server...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    print("Vítejte v systému ostraVABANK")
    print(f"Server naslouchá na {HOST}:{PORT}")
    logging.info(f"Server naslouchá na {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        logging.info(f"Připojen klient: {addr}")
        print(f"Nový klient: {addr}")
        # Každý klient má svoje vlákno.
        Thread(target=handle_client, args=(client_socket, addr)).start()


# nesahat, díky
if __name__ == "__main__":
    start_server()
