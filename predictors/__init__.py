from base_predictor import BasePredictor
from simple_history_predictor import SimpleHistoryPredictor

predictors = {
    'simple_history_predictor': SimpleHistoryPredictor(),
    'base_predictor': BasePredictor(),
}

def predictors_string():
    result = ""
    for predictor in predictors.keys():
        result += "%s \n" % predictor
    return result

def load_predictor(predictor_name):
    if predictor_name in predictors:
        return predictors[predictor_name]
    else:
        raise Error("No predictor called '%s'" % predictor_name)