#!/usr/bin/python
'''blackJack.py let's user play a game of Black Jack against a dealer'''

import random, logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
playersHand = 0
logging.disable(level=logging.CRITICAL)

def generate_cards():
	'''Generation of all existing playing cards. Problably reading from config file could
	be  better but it doesn't matter for this moment.

	One playing card will be represented by dictionary {number, pip, name, abbr, (values,)}.

	No input
	Output: List of playing cards - reusable in repeating games.

	>>> c = generate_cards()
	>>> len(c)
	52
	>>> c[1]['abbr']
	'3♥'
	>>> c[11]['values']
	(10,)
	>>> c[12]['values']
	(11, 1)
	'''

	all_cards = []
	colors = [('hearts', '♥'), ('diamonds', '♦'), ('spades', '♣'), ('clubs', '♠')]
	cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']

	for color in colors:
		for card in cards:
			# This is quick and dirty! Make it nicer some day :-)
			if type(card) is int:
				values = (card, )
			elif card in ('Jack', 'Queen', 'King'):
				values = (10, )
			else:
				values = (11, 1)

			new_card = {
				"number": str(card),
				"pip": color[0],
				"name": str(card) + ' of ' + color[0],
				"abbr": (str(card) if type(card) is int else card[0]) + color[1],
				"values": values
			}
			all_cards.append(new_card)
	return all_cards

def prepare_deck(all_cards):
	'''Prepare a new deck for a game and shuffle cards. Repeating generation of cards doesn't occur anymore.
	Input: list cards for playing
	Output: a deck of cards
	'''
	deck = []
	deck.extend(all_cards)
	random.shuffle(deck)

	return deck

def draw_card(deck):
	'''
	Draws a card from a deck
	Input: a deck of cards (list)
	Output: one card from the deck (string)

	>>> test_deck = [{'abbr': 'a'}, {'abbr' :'b'}, {'abbr': 'c'}]
	>>> draw_card(test_deck)['abbr']
	'c'
	>>> draw_card(test_deck)['abbr']
	'b'
	'''
	drawn_card = deck.pop() # get and remove last card of a list (this has been already shuffled)
	logging.debug("'{}' have been drawn and scratched from the deck".format(drawn_card['abbr']))
	return drawn_card

def hand_value(hand):
	'''
	Counts total value of all cards in hand. Uses function 'cardValue' in the process.
	Input: list of all cards in a hand (list)
	Output: total number of points in a hand (integer)

	>>> hand_value([{"values": (10,)}, {"values": (8,)}])
	18
	>>> hand_value([{"values": (10,)}, {"values": (8,)}, {"values": (3, )}])
	21
	>>> hand_value([{"values": (10,)}, {"values": (11, 1)}]) 
	21
	>>> hand_value([{"values": (11, 1)}, {"values": (11, 1)}]) 
	12
	>>> hand_value([{"values": (10,)}, {"values": (8,)}, {"values": (11, 1)}]) 
	19
	>>> hand_value([{"values": (10,)}, {"values": (8,)}, {"values": (5, )}])
	23
	>>> hand_value([{"values": (11, 1)}, {"values": (8,)}, {"values": (5, )}, {"values": (10, )}])
	24
	>>> hand_value([{"values": (11, 1)}, {"values": (9,)}, {"values": (11, 1)}])
	21
	'''
	sum = 0

	for card in sorted(hand, key=lambda c: len(c['values'])):
		s_value = card['values'][0]
		for value in card['values'][1:]: # for one-valued card result of slice is an empty tuple and for cycle is skipped
			if sum + s_value > 21:
				s_value = value
		sum += s_value

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

	if hand_value(CPUhand) > hand_value(humanHand):
		move = options[1]
		logging.debug('Banker has more points than player - it will not draw a card')

	if hand_value(CPUhand) == hand_value(humanHand):

		if len(CPUhand) > len(humanHand):
			move = options[1]
			logging.debug('Banker has same points as the player and more cards - it will draw a card')

		if len(CPUhand) <= len(humanHand):
			move = options[0]
			logging.debug('Banker has same points and same\/less cards than the player - it will not draw')

	if hand_value(CPUhand) < hand_value(humanHand):
		move = options[0]
		logging.debug('Banker has less points than the player - it will draw a card')
	return move

def hand_status(player = {"name": "Player", "role": "player", "hand": []}):
	'''Returns a text message with cards and total points.
	
	Parameters
	----------
	hand : list
		hand is a list of cards. Every card is represented as a dictionary, this 
		function expect presence of 'abbr' key and 'value' consequently.
	player: dictionary

	Returns
	-------
	string
		Human readable string to be displayed to player.	
	'''
	if player['role'] == "player":
		status = "You have {} in your hand which makes a {}-point hand."
	else:
		status = "The dealer has {} in his hand which makes a {}-point hand."
	status = status.format([h['abbr'] for h in player['hand']], hand_value(player['hand']))
	return status


def show_results(handPlayer, handCPU):
	'''
	Prints out a result of a single game of blackjack. Uses function 'resolveGame' in the process.
	Input: two final hands to be resulted (lists)
	Output: prints out value a player's and banker's hand.
	'''

	print('You have {} in you hand which makes a {}-point hand'.format([h['abbr'] for h in handPlayer], hand_value(handPlayer)))
	print('The banker has {} in his hand which makes a {}-point hand'.format([h['abbr'] for h in handCPU], hand_value(handCPU)))
	resolveGame(handPlayer, handCPU)


def resolveGame(handPlayer, handCPU):
	'''
	Decides the result of a single game.
	Input: two final hands to be resulted (lists)
	Output: prints out a message with results of the game
	'''

	print('-------GAME RESULTS-------')
	print('Your hand is {}. That\'s {} points.'.format([h['abbr'] for h in handPlayer], hand_value(handPlayer)))
	print('Banker\'s hand is {}. That\'s {} points.'.format([h['abbr'] for h in handCPU], hand_value(handCPU)))

	if hand_value(handPlayer) > 21:
		print('Sorry, you are busted with {}-point hand.'.format(hand_value(handPlayer)))

	elif hand_value(handPlayer) == 21 and len(handPlayer) == 2: # checks for straight blackjack and if so ends the game
		print('Blackjack, you win!')

	elif hand_value(handPlayer) > hand_value(handCPU):
		print('Congratulations, you win.')

	elif hand_value(handPlayer) == hand_value(handCPU):
		if len(handPlayer) < len(handCPU):
			print('Congratulations, you win.')
		if len(handPlayer) < len(handCPU):
			print('Bad luck, you lose this time.')

	elif hand_value(handPlayer) < hand_value(handCPU) and hand_value(handCPU) <= 21:
		print('Bad luck, you lose this time.')

	elif hand_value(handPlayer) < hand_value(handCPU) and hand_value(handCPU) > 21:
		print('Congratulations, you win and as a bonus the banker is busted.')

def play_game():
	'''Plays a single round of blackjack. Uses all the functions above.
	Input: User input according to the instructions printed out
	Output: Let's user play a single round of blackjack
	'''

	all_cards = generate_cards()
	deck = prepare_deck(all_cards)
	
	# Represent players as a dictionary. May be the hand shouldn't be part of this dictionary?
	# TODO: dynamic number of players with various names
	players = [
		{"name": "John Doe", "role": "player", "hand": []},
		{"name": "Anonymous Dealer", "role": "dealer", "hand": []}
	]

	for i in range(0, 2):
		for player in players:
			player['hand'].append(draw_card(deck))

	print(hand_status(players[0]))
	playerAnswer = ''

	for player in [p for p in players if p['role'] == "player"]:
		while hand_value(player['hand']) < 21 and playerAnswer != 'no': # keep playing until player says yes or has 21 or more points
			print('Would you like to draw a card? Please answer \'yes\' or \'no\'')
			playerAnswer = input().lower()

			while playerAnswer not in ['yes', 'no']: # checks that player answered yes or no
				print('I\'m sorry I don\'t understand. Please answer \'yes\' or \'no\'')
				playerAnswer = input()

			if playerAnswer == 'yes': # draws a card if player says yes
				player['hand'].append(draw_card(deck))
				print(hand_status(players[0]))

	if hand_value(playerHand) == 21 and len(playerHand) != 2: # checks for a 21-point hand other than straight blackjack. If so let's banker play
#		print('You have got 21 points but not a straight Blackjack.')
		move = bankerAI(playerHand, bankerHand) # stores the decision of AI whether to draw or unfold

		while move == 'draw': # if AI decides to draw, draws and re-evalutes the situation after new card is added to banker's hand
			bankerHand.append(draw_card(deck))
			move = bankerAI(playerHand, bankerHand)

	if playerAnswer == 'no': # stops drawing cards for the player and let's banker play
#		print('Okay, you have {}-point hand'.format(hand_value(playerHand)))
		move = bankerAI(playerHand, bankerHand) # stores the decision of AI whether to draw or unfold
		logging.debug('Banker will {}'.format(move))

		while move == 'draw': # if AI decides to draw, draws and re-evalutes the situation after new card is added to banker's hand
			bankerHand.append(draw_card(deck))
			move = bankerAI(playerHand, bankerHand)

	for card in playerHand, bankerHand: # check if cards in the game did not stay in the deck
		if card in deck:
			logging.debug('Oh no, a card has not been scratched from the deck properly')

	show_results(playerHand, bankerHand)

if __name__ == "__main__":
	# some automated tests before playing a game
	import doctest
	doctest.testmod()

	# let's go play
	print('Hi, are you up for a game of blackjack? If so just say \'yes\'') # welcome message
	oneMoreGame = input().lower() # stores players answer in lower case letter

	while oneMoreGame == 'yes':
		play_game()
		print('Are you up for one more game?')
		oneMoreGame = input().lower()

	print('Thanks for the game(s), see you soon.')
