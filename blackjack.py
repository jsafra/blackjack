#!/usr/bin/python
'''blackJack.py let's user play a game of Black Jack against a dealer'''

import random, logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
playersHand = 0
#logging.disable(level=logging.CRITICAL)

# create a new deck of cards
deck = []


# deal two cards to the player
for i in range(2):
    playersHand = playersHand + random.randint(2, 10)
    logging.debug('Player has ' + str(playersHand) + ' points')
print('You were dealt cards with total value of ' + str(playersHand))

# ask player to draw as long as he wants or until he gets busted
while playersHand < 22:
    if playersHand == 21:
        print('Congratulations, you won!')
        break
    print('Would you like to draw one more card? If so type in \'yes\'' )
    playersAnswer = input()
    logging.debug('Player answered ' + playersAnswer)     
    if playersAnswer.lower() == 'yes':
        newCard = random.randint(2,10)
        print('You have drawn ' + str(newCard))
        playersHand = playersHand + newCard
        print('You now have cards with total value of ' + str(playersHand))
    if playersAnswer.lower() == 'no':
        print('Okay, your final hand is ' + str(playersHand))
        break
    logging.debug('PlayersAnswer is ' + playersAnswer)
    if playersAnswer.lower() != 'yes' and playersAnswer.lower() !='no':
        print('I\'m sorry, I don\'t understand. Please answer \'yes\' or \'no\'')

print('Thank you for playing')
