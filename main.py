import socket
import pyodbc
from threading import Thread
import logging
import json

# Logging Configuration
logging.basicConfig(
    filename="bank_log.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

with open("config.json") as f:
    DB_CONFIG = json.load(f)

# Function to establish database connection
def get_db_connection():
    conn_str = f"DRIVER={{SQL Server}};SERVER={DB_CONFIG['SERVER']};DATABASE={DB_CONFIG['DATABASE']};UID={DB_CONFIG['USERNAME']};PWD={DB_CONFIG['PASSWORD']}"
    return pyodbc.connect(conn_str)

# Server Configuration
HOST = "192.168.1.23"
PORT = 65525
TIMEOUT = 120

# Function to execute SQL queries
def execute_query(query, params=(), fetch=False):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    if fetch:
        result = cursor.fetchall()
        conn.close()
        return result
    conn.commit()
    conn.close()

# Command Handler
def handle_command(command, client_socket, client_ip):
    try:
        parts = command.strip().split()
        response = parts[0].upper()

        if response == "BC":
            ip = client_socket.getsockname()[0]
            response = f"BC {ip}"

        elif response == "AC":
            # Create a new account with an auto-incremented account number
            last_account = execute_query("SELECT MAX(account_number) FROM Accounts", fetch=True)
            account_number = (last_account[0][0] + 1) if last_account[0][0] else 10000
            execute_query("INSERT INTO Accounts (account_number, balance) VALUES (?, 0)", (account_number,))
            response = f"AC {account_number}/{HOST}"

        elif response == "AD":
            # Deposit money
            account, amount = int(parts[1].split('/')[0]), int(parts[2])
            execute_query("UPDATE Accounts SET balance = balance + ? WHERE account_number = ?", (amount, account))
            response = "AD"

        elif response == "AW":
            # Withdraw money
            account, amount = int(parts[1].split('/')[0]), int(parts[2])
            balance = execute_query("SELECT balance FROM Accounts WHERE account_number = ?", (account,), fetch=True)
            if balance and balance[0][0] >= amount:
                execute_query("UPDATE Accounts SET balance = balance - ? WHERE account_number = ?", (amount, account))
                response = "AW"
            else:
                response = "ER Nedostatek prostředků nebo účet neexistuje."

        elif response == "AB":
            # Get account balance
            account = int(parts[1].split('/')[0])
            balance = execute_query("SELECT balance FROM Accounts WHERE account_number = ?", (account,), fetch=True)
            response = f"AB {balance[0][0]}" if balance else "ER Účet neexistuje."

        elif response == "AR":
            # Delete account if balance is 0
            account = int(parts[1].split('/')[0])
            balance = execute_query("SELECT balance FROM Accounts WHERE account_number = ?", (account,), fetch=True)
            if balance and balance[0][0] == 0:
                execute_query("DELETE FROM Accounts WHERE account_number = ?", (account,))
                response = "AR"
            else:
                response = "ER Účet nelze smazat, zůstatek není nulový."

        elif response == "BA":
            # Get total balance of all accounts
            total = execute_query("SELECT SUM(balance) FROM Accounts", fetch=True)
            response = f"BA {total[0][0] if total[0][0] else 0}"

        elif response == "BN":
            # Get number of accounts
            count = execute_query("SELECT COUNT(*) FROM Accounts", fetch=True)
            response = f"BN {count[0][0]}"

        else:
            response = "ER Neznámý příkaz."

    except Exception as e:
        response = "ER Meznámý příkaz."
        logging.error(f"Chyba: {str(e)}")

    # Send response to client
    client_socket.send(response.encode("utf-8"))
    logging.info(f"{client_ip} použil příkaz: {command.strip()} -> Odpověď zní: {response}")

# Client Handler
def handle_client(client_socket, client_ip):
    try:
        client_socket.settimeout(TIMEOUT)
        while True:
            data = client_socket.recv(1024).decode("utf-8")
            if not data:
                break
            handle_command(data, client_socket, client_ip)
    except Exception as e:
        logging.warning(f"Chyba při komunikaci s klientem {client_ip}: {str(e)}")
    finally:
        client_socket.close()

# Start Server
def start_server():
    try:
        logging.info("Spouští se server...")
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen(60)
        get_db_connection()
        logging.info(f"Server naslouchá na {HOST}:{PORT}")
    except Exception as e:
        logging.error(f"Chyba při spouštění serveru: {str(e)}")

    print("Bankovní systém ostraVABANK úspěšně spuštěn")
    print(f"Server naslouchá na {HOST}:{PORT}")
    while True:
        client_socket, client_ip = server.accept()
        logging.info(f"Připojen klient: {client_ip}")
        Thread(target=handle_client, args=(client_socket,client_ip)).start()

if __name__ == "__main__":
    start_server()
