# ostraVABANK
P2P bank system project made by Petr Kočovský for SPŠE JEČNÁ.
## Overview (Ostrava and vanbank, get it? HAHAHA)
This project is a simple P2P bank system server application designed to interact with clients over TCP sockets and perform operations on a Microsft SQL Server. It allows clients to manage bank accounts by sending simple commands, which the server processes and responds to accordingly. The application supports operations like creating new accounts, adjusting balances, querying account balances, and more.

## Features

- Account Management: Create accounts, view balances, and perform deposits or withdrawals.
- Transaction Logging: All actions are logged into a bank_log.log file for tracking and troubleshooting.
- Server Configuration: Customizable settings for the server (host, port) and database connection via configuration files.
- Client Command Handling: The server can handle multiple clients simultaneously using threads. It processes various commands from clients such as:

| Name    | Command | Description|
| -------- | ------- |------- |
| Bank code  | BC    |Get the IP Address of the bank|
| Account create | AC      |Create an account|
| Account deposit    | AD <account_number>/<ip_address> <number_of_money>  |Deposit money to specified account|
| Account withdrawal    | AW <account_number>/<ip_address> <number_of_money>   |Withdraw money from specified account|
| Account balance    | AB <account_number>/<ip_address>     |Get the balance of specified account|
| Account remove   | AR <account_number>/<ip_address>    |Remove account|
| Bank (total) amount    | BA    |Get the total amount of funds in this bank|
| Bank number of client   | BN    |Get the total amount of accounts in this bank|

## Requirements

- Python 3.x
- pyodbc (Will be automatically installed if it´s missing)
- SQL Server database (preferably Microsoft SQL Server)
- Computer (Windows, macOS, Linux) (Who would have thought)
- Internet


## Setup

You need to have an SQL Server with this query implemented:

    CREATE TABLE Accounts (
    account_number INT PRIMARY KEY,
    balance BIGINT NOT NULL DEFAULT 0
);

### Server part

Install the required dependencies: (Optional, the program will automatically install it) 

    pip install pyodbc

Configure the database and IP settings:

- insert your database connection settings in a db_config.json file.

        {
        "SERVER": "YOUR_SERVER_NAME",
        "DATABASE": "YOUR_DATABASE_NAME",
        "USERNAME": "YOUR_USERNAME",
        "PASSWORD": "YOUR_PASSWORD"
        }

- Set the server IP configuration in the ip_config.json file.

        {
        "HOST": "YOUR_IP_ADDRESS",
        "PORT": "YOUR_PORT" (Somewhere between 65525 and 65535)
        "TIMEOUT": "IN_SECONDS"
        }

Start the server:

    python main.py

The server will begin listening on the specified IP and port.

### Client Part

#### Windows

Download PuTTY from their website -> https://www.putty.org/

After downloading it, open it and type the IP Address and port of your server. From Connection Type click Other: RAW

Click Open

#### macOS and Linux

Open terminal and type:

    telnet YOUR_IP_ADDRESS YOUR_PORT
    
Hit enter.

## Sources

https://stackoverflow.com/questions/42339876/error-unicodedecodeerror-utf-8-codec-cant-decode-byte-0xff-in-position-0-in

https://stackoverflow.com/questions/1334012/cannot-insert-explicit-value-for-identity-column-in-table-table-when-identity

https://stackoverflow.com/questions/46419607/how-to-automatically-install-required-packages-from-a-python-script-as-necessary

https://stackoverflow.com/questions/39261659/how-to-send-and-receive-newline-character-over-sockets-in-a-client-server-model

https://stackoverflow.com/questions/33725862/connecting-to-microsoft-sql-server-using-python

https://stackoverflow.com/questions/43330897/oserror-winerror-10022-an-invalid-argument-was-supplied-windows-10-python

https://stackoverflow.com/questions/33932508/string-indexing-why-s00-works-and-s11-fails

https://stackoverflow.com/questions/11451101/retrieving-data-from-sql-using-pyodbc

https://stackoverflow.com/questions/3432102/python-socket-connection-timeout

https://www.geeksforgeeks.org/logging-in-python/

https://stackoverflow.com/questions/19078170/how-would-you-save-a-simple-settings-configuration-file-in-python

https://chatgpt.com/share/67a649f8-c6fc-800a-a931-979d6533bcbd

https://chatgpt.com/share/67a64a75-6f44-800a-b365-3b37a41ee402

https://chatgpt.com/share/67a64c5a-0b5c-800a-aec5-7689260eb7fe

https://realpython.com/intro-to-python-threading/

https://stackoverflow.com/questions/69923217/what-exactly-is-the-purpose-of-setsockopt

https://www.youtube.com/watch?v=eDXX5evRgQw&pp=ygUGcHlvZGJj

Reused code can be found in folder *reused*.




