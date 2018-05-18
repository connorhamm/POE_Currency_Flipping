import re
import urllib

# Initialize Currency Database
currency_database = ['Orb of Alteration', 'Orb of Fusing', 'Orb of Alchemy', 'Chaos Orb', 'Gemcutter\'s Prism',
                     'Exalted Orb', 'Chromatic Orb', 'Jeweller\'s Orb', 'Orb of Chance', 'Cartographer\'s Chisel',
                     'Orb of Scouring', 'Blessed Orb', 'Orb of Regret', 'Regal Orb', 'Divine Orb', 'Vaal Orb',
                     'Scroll of Wisdom', 'Portal Scroll', 'Armourer\'s Scrap', 'Blacksmith\'s Whetstone',
                     'Glassblower\'s Bauble', 'Orb of Transmutation', 'Orb of Augmentation', 'Mirror of Kalandra',
                     'Eternal Orb', 'Perandus Coin', 'Silver Coin', 'Sacrifice at Dusk', 'Sacrifice at Midnight',
                     'Sacrifice at Dawn', 'Sacrifice at Noon', 'Mortal Grief', 'Mortal Rage', 'Mortal Hope',
                     'Mortal Ignorance', 'Eber\'s Key', 'Yriel\'s Key', 'Inya\'s Key', 'Volkuur\'s Key',
                     'Offering to the Goddess', 'Fragment of the Hydra', 'Fragment of the Phoenix',
                     'Fragment of the Minotaur', 'Fragment of the Chimera', 'Apperentifce Cartographer\'s Sextant',
                     'Journeyman Cartographer\'s Sextant', 'Master Cartographer\'s Sextant', 'Sacrifice set',
                     'Mortal set', 'Pale Court set', 'Shaper set', 'Splinter of Xoph', 'Splinter of Tul',
                     'Splinter of Esh', 'Splinter of Uul-Netol', 'Splinter of Chayula', 'Blessing of Xoph',
                     'Blessing of Tul', 'Blessing of Esh', 'Blessing of Uul-Netol', 'Blessing of Chayula',
                     'Xoph\'s Breachstone', 'Tul\'s Breachstone', 'Esh\'s Breaschstone', 'Uul-Netol\'s Breachstone',
                     'Chayula\'s Breachstone', 'Ancient Reliquary Key', 'Divine Vessel', 'Orb of Annulment',
                     'Orb of Binding', 'Orb of Horizons', 'Harbinger\'s Orb', 'Engineer\'s Orb', 'Ancient Orb',
                     'Annulment Shard', 'Mirror Shard', 'Exalted Shard']


#################################################
# Purpose: Store Website's HTML Code into String#
# Then using regex to filter for sell/buy       #
# values, then return ratio                     #
# Params:                                       #
# "league" - Desired League for Flipping,       #
# "item1" && "item2" - Items Selected to Flip   #
# "queue" - Order based on best trade ratio     #
#################################################
def read_website(league, item1, item2, queue):
    connection = urllib.urlopen("http://currency.poe.trade/search?league="+league +"&online=x&want="+str(item1) +"&have="+str(item2) )
    output = connection.read()

    temp1 = [m1.start() for m1 in re.finditer('data-sellvalue=\"', output)]
    temp2 = [m2.start() for m2 in re.finditer('" data-buycurrency=\"', output)]
    sell = float(output[temp1[queue]+16:temp2[queue]])
    #print(sellvalue)
    
    temp3 = [m3.start() for m3 in re.finditer('data-buyvalue=\"', output)]
    temp4 = [m4.start() for m4 in re.finditer('" data-ign=\"', output)]
    buy= float(output[temp3[queue]+15:temp4[queue]])
    #print(buyvalue)

    return buy / sell

#################################################
# Purpose: Output buy/sell info for POE Shop    #
# Params:                                       #
# "league" - Desired League for Flipping,       #
# "item1" && "item2" - Items Selected to Flip   #
# "queue" - Order based on best trade ratio     #                                      
#################################################
def calculate(league, item1, item2, queue):
    ratio1 = read_website(league, item1, item2, queue)
    #print(ratio1)
    ratio2 = 1/(read_website(league, item2, item1, queue))
    #print(ratio2)

    sell_1 = ratio1
    buy_2 = 1
    sell_2 = 1
    buy_1 = ratio2

    #if profit isnt over 5c double ratio
    profit = sell_1 - buy_1
    while(profit < 10):
        sell_1 *= 2
        buy_2 *= 2
        sell_2 *= 2
        buy_1 *= 2
        profit = sell_1 - buy_1
    return (sell_1, sell_2, buy_1, buy_2)
    
#############################################################################
# Init Variables
queue = 5 #queue
item1 = 1 # Item1
item2 = 4 # Item2
total = 56 # Total Items Flipped
# Flipping Chaos Ratios with at min 5c profit per trade
while item1 != total:
    flag = 1
    while(flag):
        # exception for low quantity traded items
    	if (item1 == 4 or item1 == 24 or item1 == 25 or item1 == 26 or \
	    item1 == 36 or item1 == 37 or item1 == 38 or item1 == 39 or \
	    item1 == 50):
            item1 += 1
    	else:
	    flag = 0

    # Calculate buy and sell values
    sell_1, sell_2, buy_1, buy_2 = calculate("Abyss", item1, item2, queue)

    # Interface
    print("(sell) " + currency_database[item1-1] + " " + str(sell_2) +" <-----> " + str(buy_1) + " " + currency_database[item2-1] + " (buy) ")
    print("(sell) " + currency_database[item2-1] + " " + str(sell_1) +" <-----> " + str(buy_2) + " " + currency_database[item1-1] + " (buy) ")

    item1+=1

