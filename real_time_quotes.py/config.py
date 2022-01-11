pkey= "PKFP01KBXFK6FTYZZAXU"
skey= "UhqDY1oqZZiqczpxBcQEPPLzUEiPjpInus6ibJIe" 

Headers = {
    "APCA-API-KEY-ID": pkey,
    "APCA-API-SECRET-KEY": skey
}

BARS_URL = 'https:// data.alpaca.markets/v2/stocks/{symbol}/bars'

# {"action": "auth", "key": "PKFP01KBXFK6FTYZZAXU", "secret": "UhqDY1oqZZiqczpxBcQEPPLzUEiPjpInus6ibJIe"}

# {"action": "listen","data": {"streams": "AM.SPY"}}

# wss://stream.data.alpaca.markets/v2/iex

# {"action":"subscribe","trades":[<symbol>],"quotes":["AMD","CLDR"],"bars":["AAPL","VOO"]}