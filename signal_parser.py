import json
import re
from datetime import datetime

# Example message
message = """
GOLD  SELL  NOW  2600

LIMIT TRADE         2604

TP   ✅  2594
TP   ✅  2592
TP   ✅  2587

SL    🚫      2610

100% CONFIRM SIGNAL

USE FOR A BIG LOT SIZE
"""

def parse_signal(message):
    # Extract action (BUY/SELL) and entry price
    action_match = re.search(r'GOLD\s+(\w+)\s+NOW\s+(\d+)', message)
    action = action_match.group(1) if action_match else None
    entry_price = action_match.group(2) if action_match else None

    # Extract limit price if present
    limit_trade_match = re.search(r'LIMIT TRADE\s+(\d+)', message)
    limit_trade = limit_trade_match.group(1) if limit_trade_match else None

    # Extract take profit levels (TP)
    take_profit_matches = re.findall(r'TP\s+✅\s+(\d+)', message)
    take_profit = [int(tp) for tp in take_profit_matches]

    # Extract stop loss (SL)
    stop_loss_match = re.search(r'SL\s+🚫\s+(\d+)', message)
    stop_loss = stop_loss_match.group(1) if stop_loss_match else None

    # Construct the signal data dictionary
    signal_data = {
        "channel": "MasterOfGold52",  
        "signal": f"GOLD {action} NOW {entry_price}",
        "entry_price": int(entry_price) if entry_price else None,
        "limit_trade": int(limit_trade) if limit_trade else None,
        "take_profit": take_profit,
        "stop_loss": int(stop_loss) if stop_loss else None,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    }

    if signal_data["stop_loss"]:
        # signal_json = json.dumps(signal_data, indent=4)
        # return signal_json
        return signal_data
    return 

if __name__ == '__main__': 
    # Parse the message and convert it to JSON
    parsed_signal = parse_signal(message)
    print(parsed_signal)