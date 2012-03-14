import random

class AccuratePredictor:
    def __init__(self, accuracy):
        self.accuracy = accuracy
    
    def predict_gain(self, company, date):
        """Predicts whether company will go up or down, on the given date.
        Returns a tuple of the following form: 
            (True/False depending on predicted gain, confidence value in range [-1, 1])
        """
        gained = company.closing_price(date) > company.opening_price(date)
        if random.random() < self.accuracy:
            result = gained
        else:
            result = not gained
        return (result, 1.0)

    def __str__(self):
        return "Predictor with average accuracy of %f" % self.accuracy