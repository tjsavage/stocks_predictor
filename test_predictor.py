from datetime import datetime, timedelta
from stock_lists.company_list import CompanyList
from statlib import stats
import random, math
import smtplib
from email.mime.text import MIMEText
import sys
import predictors
from optparse import OptionParser

class ExperimentResult:
        def __init__(self, deltas, time_delta=None):
            self.deltas = deltas
            self.time_delta = time_delta
        
        def stdev(self):
            return stats.stdev(self.deltas)
        
        def mean(self):
            return stats.mean(self.deltas)
        
        def value(self, initial_value):
            final_value = initial_value
            for delta in self.deltas:
                final_value = final_value * (1 + delta)
            return final_value
        
        def profit(self, initial_value):
            return self.value(initial_value) - initial_value
        
        def daily_value(self, initial_value):
            day_value = []
            current_value = initial_value
            for delta in self.deltas:
                current_value = current_value * (1.0 + delta)
                day_value.append(current_value)
            return day_value
        
        def daily_profit(self, initial_value):
            daily_values = self.daily_value(initial_value)
            profits = []
            for day in range(len(daily_values)):
                if day == 0:
                    profit = daily_values[0] - initial_value
                else:
                    profit = daily_values[day] - daily_values[day-1]
                profits.append(profit)
            return profits
        
        def avg_daily_profit(self, initial_value):
            return stats.mean(self.daily_profit(initial_value))
        
        def prediction_accuracy(self):
            correct = 0
            for d in self.deltas:
                if d > 0:
                    correct += 1
            return correct * 1.0 / len(self.deltas)
        
        def compounded_return(self):
            result = 1.0
            for d in self.deltas:
                result = result * (1 + d)
            return result - 1.0
        
        def predicted_yearly_value(self, initial_value):
            return math.pow(1.0 + self.mean(), 270) * initial_value
                
        def __str__(self):
            result = "Prediction accuracy: %f \n" % self.prediction_accuracy()
            result += "Return: %f percent \n" % (self.compounded_return() * 100)
            result += "Mean: %f \n Stdev: %f \n Profit on $10,000: $%f" % (self.mean(), self.stdev(), self.profit(10000))
            result += "\n Avg daily profit on $10,000: $%f" % (self.avg_daily_profit(10000))
            result += "\nPredicted value after a year on $10,000: $%f" % (self.predicted_yearly_value(10000))
            if self.time_delta:
                result += "\n Elapsed: %s" % str(self.time_delta)
            return result
        
        
class Experiment:
    def __init__(self, company_list, sample_days=50, start_date=datetime.today() - timedelta(500), day_range=500, predictor=predictors.BasePredictor(), email=None, verbose=False):
        self.company_list = company_list
        self.sample_days = sample_days
        self.start_date = start_date
        self.day_range = day_range
        self.predictor = predictor
        self.email = email
        self.verbose = verbose
        
    def run_experiment(self):
        "Returns a list of daily deltas"
        start_time = datetime.now()
        deltas = []
        for day_num in range(sample_days):
            delta = None
            while delta == None:
                date = start_date + timedelta(random.randint(0, day_range))
                if self.verbose:
                    print "Trying Day %d: %s" % (day_num, date)
                delta = self.get_daily_delta(date)
                if delta:
                    deltas.append(delta)
            
        self.deltas = deltas
        elapsed = datetime.now() - start_time
        self.result = ExperimentResult(self.deltas, time_delta=elapsed)
        
        if self.email:
            self.email_result()
            
            
    def get_daily_delta(self, date):
        delta = 0
        delta_flag = False
        companies = self.company_list.get_companies()   
    
        for company in companies:
            opening = company.opening_price(date)
            closing = company.closing_price(date)
            if opening and closing:
                delta_flag = True
                predicted_gain = self.predictor.predict_gain(company, date)[0]
                if predicted_gain:
                    result = (closing - opening) / opening
                else:
                    result = 0 - (closing - opening) /opening
                delta += result
                if self.verbose:
                    print "\tResult for ticker %s" % str(company)
                    print "\t\tPredicted: %s, Actual: %s" % ("Gain" if predicted_gain else "Loss", 
                                                            "Gain" if result > 0 else "Loss")
                    print "\t\tResult: %f" % (result)
            if self.verbose and delta_flag:
                print "\tDaily Result: %f" % delta

        if delta_flag:
            return delta
    
    def email_result(self):
        user = "stocks@taylorsavage.com"
        password = 'pali2009adm'
        
        email_body = str(self) + "\n\n" + str(self.result)
        
        msg = MIMEText(email_body)
        msg['Subject'] = "Stock Experiments Result"
        msg['From'] = "stocks@taylorsavage.com"
        msg['To'] = self.email
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(user, password)
        server.sendmail(user, self.email, msg.as_string())
        server.close()
        
        print "Sent email to %s" % self.email
    
    def print_result(self):
        print str(self.result)
        
    def __str__(self):
        return "Experiment: Investing in %s using %s, %d day sample, %d day population beginning %s." % (str(self.company_list),
                                                                        str(self.predictor),
                                                                        self.sample_days,
                                                                        self.day_range,
                                                                        str(self.start_date))
                                                                    
        

if __name__ == "__main__": 
    parser = OptionParser(usage="%prog [options]")
    parser.add_option("-a", "--accuracy", action="store", 
                        type="float", dest="accuracy", default=0,
                        help="Use predictor with set ACCURACY", metavar="ACCURACY")
    parser.add_option("-e", "--email", action="store",
                        type="string", dest="email", default=None,
                        help="Send the results to EMAIL", metavar="EMAIL")
    parser.add_option("-v", "--verbose", action="store_true",
                        dest="verbose",
                        default=False, help="make lots of noise [default]")
    parser.add_option("-t", "--tickers", action="store",
                        default="^NDX", dest="tickers",
                        help="List (comma-separated) of tickers to invest in")
    parser.add_option("-s", "--sample", action="store",
                        type="int", dest="sample_days", default=30,
                        help="Sample size (# of days to choose)")
    parser.add_option("-r", "--day_range", action="store",
                        type="int", dest="day_range", default=300,
                        help="Population size (# of days to look at, starting from start date")
    parser.add_option("-d", "--date", action="store",
                        type="string", dest="start_date", default="1/1/2011",
                        help="Starting date for the experiment (format: mm/dd/YYYY)")
    parser.add_option("-p", "--predictor", action="store",
                        type="string", dest="predictor_name", default="base_predictor",
                        help="Name of the predictor to use. Predictors include: %s" % predictors.predictors_string())
    (options, args) = parser.parse_args()
    
    start_date = datetime.strptime(options.start_date, '%m/%d/%Y')
    sample_days = int(options.sample_days)
    day_range = int(options.day_range)
    company_list = CompanyList(input_str=options.tickers)
    if options.accuracy:
        predictor = predictors.AccuratePredictor(options.accuracy)
    else:
        predictor = predictors.load_predictor(options.predictor_name)
    email = options.email
    
    exp = Experiment(company_list, sample_days, start_date, day_range, predictor, email, verbose=options.verbose)
    exp.run_experiment()
    print str(exp)
    exp.print_result()