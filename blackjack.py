#!/usr/bin/python
'''blackJack.py let's user play a game of Black Jack against a dealer'''

import random, logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
playersHand = 0
logging.disable(level=logging.CRITICAL)

def createDeck():
	'''
	Creates a new deck for a  game
	No input
	Output: a deck of cards (list named 'deck')
	'''
	deck = []
	colors = ['hearts', 'diamonds', 'spades', 'clubs']
	cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']

	for color in colors:
		for card in cards:
			newCard = str(card) + ' of ' + color
			deck.append(newCard)
	return deck

def cardValue(card):
	'''
	Establishes a value of a card according to blackjack rules
	Input: a card from a deck (string)
	Output: number representing a value of the card (integer)
	'''
	if card[:2].strip().isnumeric() == True: # get value of cards beginning with number
		value = int(card[:2])
		return value

	if card[:4] in ['Jack', 'King'] or card[:5] in ['Queen']: # get value of Jack, Queen, and King
		value = 10
		return value

	if card[:3] == 'Ace': # get value of Ace
		value = 11
		return value


def drawCard(deck):
	'''
	Draws a card from a deck
	Input: a deck of cards (list)
	Output: one card from the deck (string)
	'''
	drawnCard = random.choice(deck)
	deck.remove(drawnCard)
	logging.debug('\'{}\' have been drawn and scratched from the deck'.format(drawnCard))
	return drawnCard

def handValue(hand):
	'''
	Counts total value of all cards in hand. Uses function 'cardValue' in the process.
	Input: list of all cards in a hand (list)
	Output: total number of points in a hand (integer)
	'''
	sum = 0
	for card in hand:
		sum += cardValue(card)
	for card in hand:
		if card[:3] == 'Ace' and sum > 21:
			sum = sum - 10
	return sum

def bankerAI(handPlayer, handCPU):
	'''
	Decides whether banker should draw a card or unfold his hand.
	Input: two hands of cards (list). First list passed is a player's hand, second list is banker's
	Output: AI's decision of what to do from list of options it can make (string)
	'''
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
			move = options[0]
			logging.debug('Banker has same points and same\/less cards than the player - it will not draw')

	if handValue(CPUhand) < handValue(humanHand):
		move = options[0]
		logging.debug('Banker has less points than the player - it will draw a card')
	return move

def showResults(handPlayer, handCPU):
	'''
	Prints out a result of a single game of blackjack. Uses function 'resolveGame' in the process.
	Input: two final hands to be resulted (lists)
	Output: prints out value a player's and banker's hand.
	'''

	print('You have {} in you hand which makes a {}-point hand'.format(handPlayer, handValue(handPlayer)))
	print('The banker has {} in his hand which makes a {}-point hand'.format(handCPU, handValue(handCPU)))
	resolveGame(handPlayer, handCPU)


def resolveGame(handPlayer, handCPU):
	'''
	Decides the result of a single game.
	Input: two final hands to be resulted (lists)
	Output: prints out a message with results of the game
	'''

	print('-------GAME RESULTS-------')
	print('Your hand is {}. That\'s {} points.'.format(handPlayer, handValue(handPlayer)))
	print('Banker\'s hand is {}. That\'s {} points.'.format(handCPU, handValue(handCPU)))

	if handValue(handPlayer) > 21:
		print('Sorry, you are busted with {}-point hand.'.format(handValue(handPlayer)))

	elif handValue(handPlayer) == 21 and len(handPlayer) == 2: # checks for straight blackjack and if so ends the game
		print('Blackjack, you win!')

	elif handValue(handPlayer) > handValue(handCPU):
		print('Congratulations, you win.')

	elif handValue(handPlayer) == handValue(handCPU):
		if len(handPlayer) < len(handCPU):
			print('Congratulations, you win.')
		if len(handPlayer) < len(handCPU):
			print('Bad luck, you lose this time.')

	elif handValue(handPlayer) < handValue(handCPU) and handValue(handCPU) <= 21:
		print('Bad luck, you lose this time.')

	elif handValue(handPlayer) < handValue(handCPU) and handValue(handCPU) > 21:
		print('Congratulations, you win and as a bonus the banker is busted.')

def playGame():
	'''
	Plays a single round of blackjack. Uses all the functions above.
	Input: User input according to the instructions printed out
	Output: Let's user play a single round of blackjack
	'''

	deck = createDeck()
	playerHand = [] # list where player's card will be added
	playerHand.append(drawCard(deck))
	bankerHand = [] # list where bankers card will be added
	bankerHand.append(drawCard(deck))
	playerHand.append(drawCard(deck))
	bankerHand.append(drawCard(deck))
	print('You have {} cards in your hand with total value of {} points'.format(len(playerHand), handValue(playerHand)))
	playerAnswer = ''

	while handValue(playerHand) < 21 and playerAnswer != 'no': # keep playing until player says yes or has 21 or more points
		print('Would you like to draw a card? Please answer \'yes\' or \'no\'')
		playerAnswer = input().lower()

		while playerAnswer not in ['yes', 'no']: # checks that player answered yes or no
			print('I\'m sorry I don\'t understand. Please answer \'yes\' or \'no\'')
			playerAnswer = input()

		if playerAnswer == 'yes': # draws a card if player says yes
			playerHand.append(drawCard(deck))
			print('Your hand is {}'.format(playerHand))
			print('You have {} cards in your hand with total value of {} points'.format(len(playerHand), handValue(playerHand)))

	if handValue(playerHand) == 21 and len(playerHand) != 2: # checks for a 21-point hand other than straight blackjack. If so let's banker play
#		print('You have got 21 points but not a straight Blackjack.')
		move = bankerAI(playerHand, bankerHand) # stores the decision of AI whether to draw or unfold

		while move == 'draw': # if AI decides to draw, draws and re-evalutes the situation after new card is added to banker's hand
			bankerHand.append(drawCard(deck))
			move = bankerAI(playerHand, bankerHand)

	if playerAnswer == 'no': # stops drawing cards for the player and let's banker play
#		print('Okay, you have {}-point hand'.format(handValue(playerHand)))
		move = bankerAI(playerHand, bankerHand) # stores the decision of AI whether to draw or unfold
		logging.debug('Banker will {}'.format(move))

		while move == 'draw': # if AI decides to draw, draws and re-evalutes the situation after new card is added to banker's hand
			bankerHand.append(drawCard(deck))
			move = bankerAI(playerHand, bankerHand)

	for card in playerHand, bankerHand: # check if cards in the game did not stay in the deck
		if card in deck:
			logging.debug('Oh no, a card has not been scratched from the deck properly')

	showResults(playerHand, bankerHand)

print('Hi, are you up for a game of blackjack? If so just say \'yes\'') # welcome message
oneMoreGame = input().lower() # stores players answer in lower case letter

while oneMoreGame == 'yes':

	if oneMoreGame == 'yes':
		playGame()
	print('Are you up for one more game?')
	oneMoreGame = input().lower()

print('Thanks for the game(s), see you soon.')
