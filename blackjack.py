#!/usr/bin/env python3
from random import shuffle
"""
Simple python3 version of 21
I don't actually know the rules.
Author: Ali Raheem
Version 0.1.0
GPLv2
"""
class blackjack():
	def __init__(self, player_names, num_decks, start_purse=100):
		self.num_players = len(player_names)
		self.num_decks = num_decks
		self.start_purse = start_purse
		self.running = True
		self.deck = []
		self.players = []
		self.dealer_hand = []
		self.dealer_score = 0
		self.build_deck()
		shuffle(self.deck)
		# self.build_players_interactive()
		self.build_players(player_names)
	def add_new_deck(self):
		"""Return a list of a deck of cards without jokers"""
		suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
		cards = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
		for suit in suits:
			for card in cards:
				self.deck.append(card+' of '+suit)
	def show_hand(self, hand):
		print('Cards in hand: ', end=' ')
		for card in hand:
			print(card, end=', ')
		print()
	def deal_card(self):
		try:
			return self.deck.pop()
		except:
			print("Out of cards. Reshuffling.")
			self.build_deck()
			return self.deck.pop()
	def score_hand(self, hand):
		""" Optmize score from hand given"""
		score = 0
		aces = 0
		for card in hand:
			try:
				score += int(card.split(' ')[0])
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
			if(21 < score + 10):
				break
		return score
	def deal_cards(self):
		for player in self.players:
			player['hand'] = [self.deal_card(), self.deal_card()]
	def take_bets(self):
		for player in self.players:
			cmd = 'h'
			print("{}'s turn.".format(player['name']))
			print('You have {}.'.format(player['purse']))
			try:
				player['bet'] = int(input('How much will you bet? '))
			except:
				player['bet'] = 1
			if (player['bet'] > player['purse']):
				player['bet'] = player['purse']
			if (1 > player['bet']):
				player['bet'] = 1
			self.show_hand(player['hand'])
			while(('h' == cmd)) :
				player['score'] = self.score_hand(player['hand'])
				if( 21 < player['score'] ):
					print("{} went bust.".format(player['name']))
					player['score'] = -1
					break
				print("{}'s hand scores a {}.".format(player['name'], player['score']))
				cmd = input('Hit or stick? [h/s] ')
				if('h' == cmd):
					card = self.deal_card()
					print("Got a {}.".format(card))
					player['hand'].append(card)
	def dealer_ai(self):
		""" Put score for dealers hand in dealer_score """
		self.dealer_hand = [self.deal_card(), self.deal_card()]
		print("Dealers turn.")
		self.show_hand(self.dealer_hand)
		while(17 > self.score_hand(self.dealer_hand)):
			print("Dealer: Hit me!")
			card = self.deal_card()
			print("Dealer got a {}.".format(card));
			self.dealer_hand.append(card)
		print("Dealer: I'll stick!")
		self.dealer_score = self.score_hand(self.dealer_hand)
		self.show_hand(self.dealer_hand)
		print("Dealer's hand scores a {}.".format(self.dealer_score))
		if(21 < self.dealer_score):
			print("Dealer went bust!")
			self.dealer_score = -1
	def find_winners(self):
		""" Check if players beat dealer """
		for player in reversed(self.players):
			if((player['score'] > self.dealer_score) & (1 < player['score'])):
				print("{} wins!".format(player['name']))
				player['purse'] += player['bet']
				player['bet'] = 0
			elif((self.dealer_score > player['score']) & (1 < self.dealer_score)):
				print("Dealer beat {}".format(player['name']))
				player['purse'] -= player['bet']
				player['bet'] = 0
			else:
				print("{} drew with dealer!".format(player['name']));
				player['bet'] = 0
			if(1 > player['purse']):
				print("{} is out of the game!".format(player['name']));
				self.players.remove(player)
				self.num_players -= 1
				if (1 > self.num_players):
					self.running = False
					return
	def build_deck(self):
		""" Refresh the deck """
		for _ in range(self.num_decks):
			self.add_new_deck()
	def build_players(self, player_names):
		""" Non-interactive make players """
		for name in player_names:
			self.players.append({'name': name, 'hand': [], 'score': 0, 'purse': self.start_purse, 'bet': 0})		
	def build_players_interactive(self):
		for i in range(self.num_players):
			name = input('Player name: ')
			self.players.append({'name': name, 'hand': [], 'score': 0, 'purse': self.start_purse, 'bet': 0})
def main():
	try:
		num_decks = int(input('How many decks? '))
	except:
		print("Defaulting to 3.")
		num_decks = 3
	name = 'a'
	player_names = []
	while ('' != name):
		name = input('Enter player name: ')
		player_names.append(name)
	game = blackjack(player_names, num_decks)
	while (game.running):
		game.deal_cards()
		game.take_bets()
		game.dealer_ai()
		game.find_winners()
if "__main__" == __name__:
	main()
