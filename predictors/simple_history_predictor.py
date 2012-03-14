from base_predictor import BasePredictor
from datetime import datetime, timedelta

class SimpleHistoryPredictor(BasePredictor):
    """Predicts based on the opposite of what the stock did the previous trading day"""
    def __init(self):
        pass
    
    def predict_gain(self, company, date):
        previous_date = date
        previous_gain = None
        while(previous_gain is None):
            previous_date -= timedelta(days=1)
            previous_gain = company.daily_change(previous_date) > 0
        return (not previous_gain, 1)