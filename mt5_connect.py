import MetaTrader5 as mt5

# 1. Initialize the MT5 connection
mt5.initialize()

# 2. Login to the demo account


class MT5TradingBot:
    def __init__(self, account, password, server):
        self.account = account
        self.password = password
        self.server = server
        self.initialize()

    def initialize(self):
        """Initialize MT5 and login to the account."""
        if not mt5.initialize():
            print("Initialization failed")
            return
        if not mt5.login(self.account, self.password, self.server):
            print(f"Failed to connect to account {self.account}. Error: {mt5.last_error()}")
        else:
            print(f"Connected to account {self.account} on server {self.server}")

    def get_account_info(self):
        """Retrieve account information."""
        account_info = mt5.account_info()
        if account_info is None:
            print("Failed to get account information")
            return None
        return account_info

    def has_open_trade(self, symbol):
        """Check if there is an open trade for the given symbol."""
        positions = mt5.positions_get(symbol=symbol)
        return len(positions) > 0

    def place_trade(self, signal_data):
        """Place a trade based on the provided signal data."""
        action = signal_data['signal'].split()[1]  # 'BUY' or 'SELL'
        entry_price = signal_data['entry_price']
        stop_loss = signal_data['stop_loss']
        take_profit_list = signal_data['take_profit']
        take_profit = take_profit_list[-1]
        # Use the first TP for now
        # print(type(take_profit))
        # print(take_profit[-1])
        symbol = "XAUUSD"

        if self.total_positions() > 4:
            print(f"Trade already open for {symbol}. Not placing a new trade.")
            return

        order_type = mt5.ORDER_TYPE_BUY if action == 'BUY' else mt5.ORDER_TYPE_SELL

        price = mt5.symbol_info_tick(symbol).ask if order_type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).bid

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": 2.0,  # Define your lot size
            "type": order_type,
            "price": price,
            "sl": float(price - 5),
            "tp": float(price + 15),
            "deviation": 10,
            "magic": 234000,
            "comment": "Signal trade",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
                
        result = mt5.order_send(request)
        # print(result)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Failed to place order: {result.retcode}")
        else:
            print(f"Order placed successfully: {result.order}")

    def place_simple_trade(self, symbol="XAUUSD", volume=0.1, action='BUY'):
        """Place a simple trade for BTCUSD."""
        # Determine the order type
        order_type = mt5.ORDER_TYPE_BUY if action == 'BUY' else mt5.ORDER_TYPE_SELL
        print(order_type)
        # Get the current price
        price = mt5.symbol_info_tick(symbol).ask if order_type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).bid

        print(price)
        # Prepare the order request
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": 2.0,
            "type": order_type,
            "price": price,
            "sl": float(price - 5),
            "tp": float(price + 15),
            "deviation": 10,
            "magic": 234000,
            "comment": "Simple BTC trade",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        # Send the order
        result = mt5.order_send(request)
        print(result)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Failed to place order: {result.retcode}")
        else:
            print(f"Order placed successfully for {symbol}: {result.order}")
    def total_positions(self):
        """Get the total number of positions."""
        positions_total = mt5.positions_total()
        if positions_total > 0:
            print("Total positions=", positions_total)
        else:
            print("Positions not found")
        return positions_total

    def get_open_position(self, symbol):
        """Retrieve an open position for the given symbol."""
        positions = mt5.positions_get(symbol=symbol)
        if positions:
            return positions[0]  # Return the first position (if there are multiple, you can modify this)
        else:
            print(f"No open positions found for {symbol}")
            return None

    def close_all_trades(self):
        """Close all open trades."""
        positions = mt5.positions_get()
        print(positions)

        if positions is None or len(positions) == 0:
            print("No open positions to close.")
            return

        for position in positions:
            symbol = position.symbol
            volume = position.volume
            position_type = position.type  # 0 = BUY, 1 = SELL

            # Reverse the order type to close the trade
            close_order_type = mt5.ORDER_TYPE_SELL if position_type == 0 else mt5.ORDER_TYPE_BUY
            price = mt5.symbol_info_tick(symbol).bid if close_order_type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(
                symbol).ask
            print(price)
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": volume,
                "type": close_order_type,
                "price": price,
                "position": position.ticket,  # Use the ticket to identify the position to close
                "deviation": 10,
                "magic": 234000,
                "comment": "Closing trade",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }

            # Send the order to close the position
            result = mt5.order_send(request)

            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print(f"Failed to close order {position.ticket}: {result.retcode}")
            else:
                print(f"Order {position.ticket} closed successfully.")
    def shutdown(self):
        """Shutdown the MT5 connection."""
        mt5.shutdown()


if __name__ == "__main__":
    from info import password, account, server
    trading_bot = MT5TradingBot(account=account, password=password, server=server)

    print(trading_bot.place_simple_trade())
    # print(trading_bot.close_all_trades())