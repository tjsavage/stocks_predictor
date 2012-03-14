import datetime
from pystockquotes import quotes

class Company:
	def __init__(self, symbol):
		self.symbol = symbol

	def current_price(self):
		return quotes.current_price(self.symbol)

	def opening_price(self, date=datetime.datetime.today()):
		return quotes.opening_price(self.symbol, date)

	def closing_price(self, date=datetime.datetime.today()):
		return quotes.closing_price(self.symbol, date)

	def __str__(self):
		return self.symbol
