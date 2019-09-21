#!/usr/bin/python
'''blackJack.py let's user play a game of Black Jack against a dealer'''

import random, logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
playersHand = 0
logging.disable(level=logging.CRITICAL)

def createDeck(): # create a new deck of cards
	deck = []
	colors = ['hearts', 'diamonds', 'spades', 'clubs']
	cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']
	for color in colors:
		for card in cards:
			newCard = str(card) + ' of ' + color
			deck.append(newCard)
	return deck

def cardValue(card): # find a value of a card
	if card[:2].strip().isnumeric() == True:
		value = int(card[:2])
		return value
	if card[:4] in ['Jack', 'King'] or card[:5] in ['Queen']:
		value = 10
		return value
	if card[:3] == 'Ace':
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

#TODO: create a function to 'pretty print' players hand
#TODO: create a function that plays for a banker

def playGame(): #plays a single game round
	deck = createDeck()
	playerHand = []
	playerHand.append(drawCard(deck))
	playerHand.append(drawCard(deck))
	print('You have {} cards in your hand.'.format(len(playerHand)))
	for card in playerHand:
		print('\'{}\''.format(card), end=', ')
	print()
	playerAnswer = ''
	while handValue(playerHand) < 21 and playerAnswer != 'no':
		print('Would you like to draw a card? Please answer \'yes\' or \'no\'')
		playerAnswer = input().lower()
		while playerAnswer not in ['yes', 'no']:
			print('I\'m sorry I don\'t understand. Please answer \'yes\' or \'no\'')
			playerAnswer = input()
		if playerAnswer == 'yes':
			playerHand.append(drawCard(deck))
	if handValue(playerHand) == 21 and len(playerHand) == 2:
		print('Blackjack, you win!')
	if handValue(playerHand) == 21 and len(playerHand) != 2:
		print('You have got 21 points but not a straight Blackjack.')
	if handValue(playerHand) > 21:
		print('Sorry, you are busted with {}-point hand.'.format(handValue(playerHand)))
	if playerAnswer == 'no':
		print('Okay, you have {}-point hand'.format(handValue(playerHand)))

print('Hi, are you up for a game of blackjack? If so just say \'yes\'')
oneMoreGame = input().lower()
while oneMoreGame == 'yes':
	if oneMoreGame == 'yes':
		playGame()
	print('Are you up for one more game?')
	oneMoreGame = input().lower()
print('Thanks for the game(s), see you soon.')
