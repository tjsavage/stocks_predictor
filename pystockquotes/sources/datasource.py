
class DataSourceAbstract(object):
	def __init__(self):
		pass
	
	def current_price(self, symbol):
		raise NotImplementedError("Datasource hasn't implemented current_price")

	def get_all(self, symbol):
		raise NotImplementedError("Datasource hasn't implemented get_all.")

	def opening_price(self, symbol, date):
		raise NotImplementedError("Datasource hasn't implemented opening_price.")

	def closing_price(self, symbol, date):
		raise NotImplementedError("Datasource hasn't implemented closing_price.")
