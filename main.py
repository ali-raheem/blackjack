#!/usr/bin/env python3
from random import shuffle


def new_deck():
	'''Return a list of a deck of cards without jokers'''
	suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
	cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
	deck = []
	for suit in suits:
		for card in cards:
			deck.append(card+' of '+suit)
	return deck
def score_hand(hand):
	''' Optmize score from hand given'''
	score = 0
	aces = 0
	for card in hand:
		try:
			score += int(card[0])
		except:
			if('A' == card[0]):
				score += 1
				aces += 1
			else:
				score += 10
	while(aces):
		if(21 >= score + 10):
			aces -= 1
			score += 10
		if(21 > score + 10):
			break
	return score
				
def main():
	num_decks = int(input('How many decks? '))
	deck = []
	for _ in range(num_decks):
		deck += new_deck()
	shuffle(deck)
	num_players = int(input('How many players? '))
	player_template = {'name': '', 'hand': []}
	players = []
	for i in range(num_players):
		players.append(player_template)
	for player in players:
		player['name'] = input('Player name: ')
		player['hand'] = [deck.pop(), deck.pop()]
	print(players)
	for player in players:
		cmd = 'h'
		print(player['name'])
		while('h' == cmd):
			print(player['hand'])
			print(score_hand(player['hand']))
			cmd = input('Hit or stick? [h/s]')
			if('h' == cmd):
				player['hand'].append(deck.pop())
		
if "__main__" == __name__:
	main()
