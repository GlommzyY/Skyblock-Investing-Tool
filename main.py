from hypixelSkyblockApiWrapper import SkyblockApi
from time import sleep

api = SkyblockApi()
minutesToWait = 10


#Get first item 
initialProducts = {}
items = api.get_bazaar()["products"]
for i in items.keys():
    itemName = i
    
    #There might not be enough orders
    try:
        sellPrice = items[i]["sell_summary"][0]["pricePerUnit"]
    except IndexError as ie:
        sellPrice = 0
    
    try:
        buyPrice = items[i]["buy_summary"][0]["pricePerUnit"]
    except IndexError as ie:
        buyPrice = 0

    initialProducts[itemName] = [sellPrice, buyPrice]

for i in range(minutesToWait):
    print("{} minutes waited out of {} ({}%)".format(i, minutesToWait, (100 * i/minutesToWait)))
    sleep(60)

#Get second item price

laterProducts = {}
items = api.get_bazaar()["products"]
for i in items.keys():
    itemName = i

    #There might not be any orders
    try:
        sellPrice = items[i]["sell_summary"][0]["pricePerUnit"]
    except IndexError as ie:
        sellPrice = 0
    
    try:
        buyPrice = items[i]["buy_summary"][0]["pricePerUnit"]
    except IndexError as ie:
        buyPrice = 0

    laterProducts[itemName] = [sellPrice, buyPrice]

resultList = []

#Compare item prices
for i in initialProducts.keys():
    sellPriceDiff = laterProducts[i][0] - initialProducts[i][0]
    
    try:
        sellPricePercentage = (laterProducts[i][0] / initialProducts[i][0]) * 100
    except ZeroDivisionError as zde:
        sellPricePercentage = 0

    buyPriceDiff = laterProducts[i][1] - initialProducts[i][1]
    
    try:
        buyPricePercentage = (laterProducts[i][1] / initialProducts[i][1]) * 100
    except ZeroDivisionError as zde:
        buyPricePercentage = 0

    resultList.append([i, sellPriceDiff, sellPricePercentage, buyPriceDiff, buyPricePercentage])

#Sorting by each category and outputing top items
bestSellPriceDiff = sorted(resultList, key= lambda x: x[1], reverse=True)[:11]
bestSellPricePercentage = sorted(resultList, key= lambda x: x[2], reverse=True)[:11]
bestBuyPriceDiff = sorted(resultList, key= lambda x: x[3], reverse=True)[:11]
bestBuyPricePercentage = sorted(resultList, key= lambda x: x[4], reverse=True)[:11]

print("\n\nTop gainers in sell order price : ")
for i in bestSellPriceDiff:
    print("{} : {} coins".format(i[0], i[1]))

print("\n\nTop percentage gainers in sell order price : ")
for i in bestSellPricePercentage:
    print("{} : {} %".format(i[0], i[2]))

print("\n\nTop gainers in buy order price : ")
for i in bestBuyPriceDiff:
    print("{} : {} coins".format(i[0], i[3]))

print("\n\nTop percentage gainers in buy order price : ")
for i in bestBuyPricePercentage:
    print("{} : {} %".format(i[0], i[4]))