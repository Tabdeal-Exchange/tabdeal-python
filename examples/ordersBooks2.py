# Name :  ordersBooks2.py
# Example by Alimogh

#import json # 
from tabdeal.spot import Spot

print("-= Prices in Tabdeal =-")
print("-= قیمتها در صرافی تبدیل =-")
client = Spot()

list_base1 = ["BTC" , "ETH" ,"BNB" ,"ADA" ,"TRX" \
,"SHIB" , "DASH" ,"ETC" ,"DGB" ,"DOGE" , "LTC"  \
,"RVN" ,"FLOW" ]
list1 = ["USDT"] # , "IRT"]

list_base2 = ["BTC" , "ETH" ,"BNB" ,"ADA" ,"TRX" ,"SHIB" ,"USDT"]
list2 = ["IRT"]

try :
	for symb1 in list_base1 :
		for symb2 in list1 :
		    symbl = symb1 + symb2
		    market = symb1 + "/" + symb2
		    order_book = client.depth(
		        symbol = symbl,
		        limit=1
		        )
		    #print(str(order_book))
		    #print(str( order_book["asks"][0]))
		    print("\nMarket : ", market)
		    print("Ask : ", str( order_book["asks"][0][0]), end="")
		    print(" / [Amount] : ", str( order_book["asks"][0][1]))
		    print("Bid : ", str( order_book["bids"][0][0]), end="")
		    print(" / [Amount] : ", str( order_book["bids"][0][1]))
		    
except :
    pass

### IRT  Toman
try :
	for symb1 in list_base2 :
		for symb2 in list2 :
		    symbl = symb1 + symb2
		    market = symb1 + "/" + symb2
		    order_book = client.depth(
		        symbol = symbl,
		        limit=1
		        )
		    print("\nMarket : ", market)
		    print("Ask : ", str( order_book["asks"][0][0]), end="")
		    print(" / [Amount] : ", str( order_book["asks"][0][1]))
		    print("Bid : ", str( order_book["bids"][0][0]), end="")
		    print(" / [Amount] : ", str( order_book["bids"][0][1]))
		    
except :
    pass
"""
return of order_book :

{'asks': [['19903.08000000', '0.00909700']], 
'bids': [['19839.79000000', '0.24334000']]}

"""

