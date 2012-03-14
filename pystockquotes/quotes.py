import datetime
from pystockquotes.sources import Yahoo 

datasource = Yahoo.DataSourceYahoo()

def set_datasource(source):
	pass

def current_price(symbol):
	return datasource.current_price(symbol)

def get_all(symbol):
	return datasource.get_all(symbol)

def opening_price(symbol, date=datetime.datetime.today()):
	return datasource.opening_price(symbol, date)

def closing_price(symbol, date=datetime.datetime.today()):
	return datasource.closing_price(symbol, date)
