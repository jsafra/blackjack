#!/usr/bin/python
'''blackJack.py let's user play a game of Black Jack against a dealer'''

import random, logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
playersHand = 0
#logging.disable(level=logging.CRITICAL)

def createDeck(): # create a new deck of cards
	deck = []
	colors = ['hearts', 'diamonds', 'spades', 'clubs']
	cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']

	for color in colors: # fill deck with every card from each color
		for card in cards:
			newCard = str(card) + ' of ' + color
			deck.append(newCard)
	return deck

def cardValue(card): # find a value of a card
	if card[:2].strip().isnumeric() == True: # get value of cards beginning with number
		value = int(card[:2])
		return value

	if card[:4] in ['Jack', 'King'] or card[:5] in ['Queen']: # get value of Jack, Queen, and King
		value = 10
		return value

	if card[:3] == 'Ace': # get value of Ace
		value = 11
		return value


def drawCard(deck): #deals a card
	drawnCard = random.choice(deck)
	deck.remove(drawnCard)
	print('You have been dealt \'{}\''.format(drawnCard))
	logging.debug('\'{}\' have been drawn and scratched from the deck'.format(drawnCard))
	return drawnCard

def handValue(hand): #counts value of cards in hand
	sum = 0
	for card in hand:
		sum += cardValue(card)
	for card in hand:
		if card[:3] == 'Ace' and sum > 21:
			sum = sum - 10
	return sum

def bankerAI(handPlayer, handCPU): # decide what move should AI make
	humanHand = handPlayer
	CPUhand = handCPU
	options = ['draw', 'unfold'] # list options CPU can make

	if handValue(CPUhand) > handValue(humanHand):
		move = options[1]
		logging.debug('Banker has more points than player - it will not draw a card')

	if handValue(CPUhand) == handValue(humanHand):

		if len(CPUhand) > len(humanHand):
			move = options[1]
			logging.debug('Banker has same points as the player and more cards - it will draw a card')

		if len(CPUhand) <= len(humanHand):
			move = option[0]
			logging.debug('Banker has same points and same\/less cards than the player - it will not draw')

	if handValue(CPUhand) < handValue(humanHand):
		move = options[0]
		logging.debug('Banker has less points than the player - it will draw a card')
	return move # returns 'draw' or 'unfold' to the calling function

def showResults(handPlayer, handCPU): # show final hands of the player and banker

	print('You have {} in you hand which makes a {}-point hand'.format(handPlayer, handValue(handPlayer)))
	print('The banker has {} in his hand which makes a {}-point hand'.format(handCPU, handValue(handCPU)))
	resolveGame(handPlayer, handCPU)


def resolveGame(handPlayer, handCPU): # decide who wins the game

	if handValue(handPlayer) > handValue(handCPU):
		print('Congratulations, you win.')
	if handValue(handPlayer) == handValue(handCPU):
		if len(handPlayer) < len(handCPU):
			print('Congratulations, you win.')
		if len(handPlayer) < len(handCPU):
			print('Bad luck, you lose this time.')
	if handValue(handPlayer) < handValue(handCPU) and handValue(handCPU) <= 21:
		print('Bad luck, you lose this time.')
	if handValue(handPlayer) < handValue(handCPU) and handValue(handCPU) > 21:
		print('Congratulations, you win and as a bonus the banker is busted.')

def playGame(): #plays a single game round

	deck = createDeck()
	playerHand = [] # list where players card will be added
	playerHand.append(drawCard(deck)) # draw first card for the player
	bankerHand = [] # list where bankers card will be added
	bankerHand.append(drawCard(deck)) # draw firs card for the player
	playerHand.append(drawCard(deck)) # draw second card for the player
	bankerHand.append(drawCard(deck)) # draw second card for the banker
	print('You have {} cards in your hand with total value of {} points'.format(len(playerHand), handValue(playerHand)))
	playerAnswer = ''

	while handValue(playerHand) < 21 and playerAnswer != 'no': # keep playing until player says yes or has 21 or more points
		print('Would you like to draw a card? Please answer \'yes\' or \'no\'')
		playerAnswer = input().lower()

		while playerAnswer not in ['yes', 'no']: # checks that the game understands player's answer
			print('I\'m sorry I don\'t understand. Please answer \'yes\' or \'no\'')
			playerAnswer = input()

		if playerAnswer == 'yes': # draws a card if player says yes
			playerHand.append(drawCard(deck))
			print('You have {} cards in your hand with total value of {} points'.format(len(playerHand), handValue(playerHand)))

	if handValue(playerHand) == 21 and len(playerHand) == 2: # checks for straight blackjack
		print('Blackjack, you win!')

	if handValue(playerHand) == 21 and len(playerHand) != 2: # checks for a 21-point hand other than straight blackjack
		print('You have got 21 points but not a straight Blackjack.')
		move = bankerAI(playerHand, bankerHand)

		while move == 'draw':
			bankerHand.append(drawCard(deck))
			move = bankerAI(playerHand, bankerHand)

		showResults(playerHand, bankerHand)

	if handValue(playerHand) > 21: # checks if player is busted
		print('Sorry, you are busted with {}-point hand.'.format(handValue(playerHand)))

	if playerAnswer == 'no': # stops drawing cards if player says so
		print('Okay, you have {}-point hand'.format(handValue(playerHand)))
		move = bankerAI(playerHand, bankerHand)
		logging.debug('Banker will {}'.format(move))

		while move == 'draw':
			bankerHand.append(drawCard(deck))
			move = bankerAI(playerHand, bankerHand)

		showResults(playerHand, bankerHand)

	for card in playerHand, bankerHand: # check if cards in the game did not stay in the deck
		if card in deck:
			logging.debug('Oh no, a card has not been scratched from the deck properly')


print('Hi, are you up for a game of blackjack? If so just say \'yes\'') # welcome message
oneMoreGame = input().lower() # stores players answer in lower case letter

while oneMoreGame == 'yes':

	if oneMoreGame == 'yes':
		playGame()
	print('Are you up for one more game?')
	oneMoreGame = input().lower()

print('Thanks for the game(s), see you soon.')
