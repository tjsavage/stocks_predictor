import pystockquotes.sources.lib.ystockquote as ystockquote
import datetime
from datasource import DataSourceAbstract

class DataSourceYahoo(DataSourceAbstract):
	def current_price(self, symbol):
		return float(ystockquote.get_price(symbol))

	def get_all(self, symbol):
		return ystockquote.get_all(symbol)

	def opening_price(self, symbol, date=datetime.datetime.today()):
		return self.get_historical_info(symbol, date=date, info_type='Open')
	
	def closing_price(self, symbol, date=datetime.datetime.today()):
		return self.get_historical_info(symbol, date=date, info_type='Close')

	def get_historical_info(self, symbol, date=datetime.datetime.today(), info_type='Close'):
		historical_info = ystockquote.get_historical_prices(symbol, date.strftime('%Y%m%d'), date.strftime('%Y%m%d'))
		try:
			info_index = historical_info[0].index(info_type)
			if info_index < 7 and info_index >= 0:
				return float(historical_info[1][info_index])
		except:
			pass
