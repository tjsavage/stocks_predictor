class BasePredictor:
    def __init__(self):
        pass
    
    def predict_gain(self, company, date):
        """Predicts whether company will go up or down, on the given date.
        Returns a tuple of the following form: 
            (True/False depending on predicted gain, confidence value in range [-1, 1])
        """
        return (True, 1.0)