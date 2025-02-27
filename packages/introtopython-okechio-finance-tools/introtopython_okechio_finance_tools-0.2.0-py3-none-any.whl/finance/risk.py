#This import will fail
#from analytics.metrics import volatility 

#To fix the import issue
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from analytics.metrics import volatility # Now it works

def risk_assessment(investment, volatility):
    return investment * volatility
