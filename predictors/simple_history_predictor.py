from base_predictor import BasePredictor

class SimpleHistoryPredictor(BasePredictor):
    def __init(self):
        pass
    
    def predict_gain(self, company, date):
        return (False, 1.0)