# GreekSoft API
Greeksoft_API is a Python-based project that allows users to subscribe to the Greek token and retrieve the latest tick data. This project helps in authenticating a user, broadcasting tokens, and placing orders in a seamless manner.

# Features Authentication: 
By passing a username, session password, and user password, the project authenticates the user.
# Token Retrieval: 
Retrieves the latest token broadcast.
# Order Placement: 
Capable of placing orders once authenticated.

# Technologies Used
Python built-in Libs & third party libs (Pandas, numpy,requests,etc.)

# What's New in Version 0.0.2
**Fixed**

**Bug Fix**: Fixed an issue where placing a new order would fail due to a regenerating the new session token. The issue is now resolved, and order requests should succeed.

```
pip install greeksoft
```

Usage
Once installed, you can use the project by importing the Greek_API from the greek_api_client package. Below is an example of how to use the API:

```
from greeksoft import Greek_API

username="username" # String Format

session_pwd="session_pwd"  #String Format

user_pwd="user_pwd" #String Format

procli="procli" # for client id procli="2", retail id procli='1'

ac_no='ac_no' # if retail id pass account number in String Format. 

api = Greek_API(username,session_pwd,user_pwd,procli,ac_no) #to authenticate the creadentials passed.

token_no='102000000' # string format

# Authenticate and fetch the latest token

token = api.token_broadcast('token_no','asset_type') # token_no in 'String', asset_type='option' or 'future' or 'equity' in string format.

# token=token['data.token'][0] <-- get token no

# symbol=token['data.symbol'][0] <-- get symbol name of token passed

# time=token['data.ltt'][0] <-- provide the time

# strike=token['data.strikeprice'][0] <-- get Strike 

# option_type=token['data.optiontype'][0] <-- get Option type CE or PE

# instrument=token['data.instrument'][0] <-- get instrument type FUTSTK,OPTSTK...

# bid_price=token[data.bid][0] <-- get bid price of token passed 

# ask_price=token['data.ask'][0] <-- get ask price of token passed


# Subscribe with the Greek Token and pass it in list eg:token_list=['','',...] into the declared variable. 

token_list=['102000000','102000000',...] # Only pass Greek Token.

for data in api.get_apollo_resp(token_list): # To get response of tokens passed of list using loop.
    print(data)
    
# Place order passing required paramets, # token_no='102000000', symbol="RELIANCE", qty="minimum_lot" for respective token,

# price= value get from bid/ask price from token broadcast against respective token,

#buysell= if buy then pass 1 and for sell 2 in integer format,

ordtype=1, trigprice=0, strategyname="example" strategy name will be anything as per userinput.

var_response=api.place_order(tokenno,symbol,qty,price,buysell,ordtype,trigprice,strategyname) # pass the required parameters
 
print(var_response) # acknowledge the response get from place order function.
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.




