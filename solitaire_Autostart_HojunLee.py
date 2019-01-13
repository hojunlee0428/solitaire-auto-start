
#imports
import random
import csv
import re
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import time

#Variables
#ASSUMTION: There are four types of suits in each deck: Spade,Heart,Diamond,and Clover
deckNum = 2     #number of decks
stackNum = 10   #number of stacks
stackSize = 4   #size of each stack
pileNum = 8     #number of piles
numSuitPile = int(pileNum/4) #number of piles for each suit
#Lists
deckInput = []   #list that contains imported cards
deck = []        #list that contains all the decks
countList = []   #list that contains the loop counts
#Dictionaries
stackLib = {}    #stack library: Dictionary that contains all the stacks        
pileLib = {}     #pile library: Dictionary that contains all the piles   



#fucntion to import a file with card deck
def openDeck(filename, array):
    with open(filename,'r') as f:
        reader = csv.reader(f)
        for row in reader:
            array.append(row[0])
#function to put all the cards in a deck list and shuffle
def shuffleCard(decknumber,deckinput,carddeck):
    for x in range(decknumber):
        carddeck.extend(deckinput)
        random.shuffle(carddeck)

#function to construct stacks with given number of stacks and cards
def makeStack(stacknumber,stackobj,carddeck):
    for i in range(1,stacknumber+1):
        stackobj['stack'+str(i)] = []
        s = stackobj.get('stack'+str(i))
        s[0:4] = carddeck[0:4]
        del carddeck[0:4]
#function to make piles for all four suits  
def makePile(num,pileobj):
    for i in range(num):
        pileobj['pileS'+str(i+1)] = []
        pileobj['pileH'+str(i+1)] = []
        pileobj['pileD'+str(i+1)] = []
        pileobj['pileC'+str(i+1)] = []




#Auto Start function for a solitare game
def autoStart(carddeck,stacknumber,stacksize,library,pilesuitnum,pilelibrary,pilecount):

    #counter for interation
    c = 0
    #iterate through the top of every stack until iteration reaches end
    while c < stacknumber:
        #initialize the array of stack tops 
        stackTops = []
        for i in (library.keys()):
            try:
                stackTops.append(library[i][-1])
            except IndexError:
                stackTops.append('0D') #dummy card for empty stacks

        card = stackTops[c] #get the current card
        cardNum = int(re.search(r'\d+', card).group()) #get number of the card
        suit = card[len(card)-1:len(card)] #get suit of the card
        prevCard = str(cardNum - 1) + suit #get card number down to the current card
        stack = library.get('stack'+str(c+1)) #get the stack the card is on top of

        
        
        #iterate through piles to see if it can be stacked on
        for i in range(pilesuitnum):
            pile = pilelibrary.get('pile'+ suit + str(i+1)) #fetch the pile according to the pile
            n = len(pile)
            pileTop = pile[-1:]
            p = [prevCard]
            #if the pile is empty and the current card number is 1 put card in the pile
            #put it on the stack and break the for loop
            if n == 0 and cardNum == 1:
                pile.append(card)
                stack.remove(stack[-1])
                pilecount+=1
                c=0          
                break
            #else if the card on top of the pile equals to previous of the current card
            #put it on the stack and break the for loop
            elif pileTop == p:
                pile.append(card)
                stack.remove(stack[-1])
                pilecount+=1
                c=0 
                break
            #if looked through all the piles, break the for loop
            elif (i+1)==pilesuitnum:
                c+=1
                break

    #return the total number of cards that were piled in autostart
    return pilecount




#MAIN




#import deck from csv
openDeck('deck.csv',deckInput)


"""
# ==================================================
#setup game
shuffleCard(deckNum,deckInput,deck) #put all the decks in deck list and shuffle it
makeStack(stackNum,stackLib,deck) #make stacks
makePile(numSuitPile,pileLib)#make piles

#test autoStart
print(stackLib,'\n') #print initial stacks
count = 0
print('Total # of cards in piles: ',autoStart(deck,stackNum,stackSize,stackLib,numSuitPile,pileLib,count),'\n')
print(stackLib,'\n') #print stacks after autoStart
print(pileLib)#print piles
# ==================================================

# ==================================================
"""
#Run autostart until it finds case with 15 moves
start = time.time() #start measuring machine running time 
loopCount = 0
while True:
    loopCount += 1
    #setup game
    deck = [] #initialize/empty the deck
    shuffleCard(deckNum,deckInput,deck) #put all the decks in deck list and shuffle it
    makeStack(stackNum,stackLib,deck) #make stacks
    makePile(numSuitPile,pileLib)#make piles

    count = 0
    pileCount = autoStart(deck,stackNum,stackSize,stackLib,numSuitPile,pileLib,count)
    countList.append(pileCount)
    if pileCount == 15: #when case with 15 moves is found, break
        break
        

end = time.time()
print('total number of loops to find 15: ', loopCount)
print(end - start)
x = countList
 

#the histogram of the data
num_bins = 20
n, bins, patches = plt.hist(x, num_bins, density=1, facecolor='blue', alpha=0.5)
#show plot
plt.xlabel('number of cards in piles')
plt.ylabel('frequency')
plt.subplots_adjust(left=0.15)
plt.show()



