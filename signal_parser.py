import re
from datetime import datetime

message = """
    **XAUUSD BUY NOW 3324

STOP LOSS    (  3314  )
"""
def parse_signal(message):
    message = message.upper()

    # Ensure "XAUUSD" is in the message
    if "XAUUSD" not in message:
        return None

    # Look for a pattern like: BUY NOW 3324 or SELL NOW 2590
    match = re.search(r'\b(BUY|SELL)\s+NOW\s+(\d+)', message)
    if not match:
        return None

    action = match.group(1)
    entry_price = int(match.group(2))

    return {
        "symbol": "XAUUSD",
        "action": action,
        "entry_price": entry_price,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

if __name__ == '__main__': 
    # Parse the message and convert it to JSON
    parsed_signal = parse_signal(message)
    print(parsed_signal)