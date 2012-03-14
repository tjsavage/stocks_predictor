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
	
	def daily_change(self, date=datetime.datetime.today()):
	    opening = self.opening_price(date)
	    if opening is not None:
	        return self.closing_price(date) - opening
	    else:
	        return None

	def __str__(self):
		return self.symbol
