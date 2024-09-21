import MetaTrader5 as mt5

# 1. Initialize the MT5 connection
mt5.initialize()

# 2. Login to the demo account
account = 1510023678
password = "9Ln!1iA71W"
server = "FTMO-Demo"

# Connect to the MT5 account
if not mt5.login(account, password, server):
    print(f"Failed to connect to account {account}. Error: {mt5.last_error()}")
else:
    print(f"Connected to account {account} on server {server}")

# 3. Get account info (balance)
account_info = mt5.account_info()

if account_info is None:
    print("Failed to get account information")
else:
    # Check balance
    print(f"Balance: {account_info.balance}")
    print(f"Equity: {account_info.equity}")

# 4. Shutdown MT5 connection
mt5.shutdown()
