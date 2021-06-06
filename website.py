from flask import Flask, render_template, request
from ComparePrices import Prices
import os

# TEMPLATE_DIR = os.path.abspath('../templates')
# STATIC_DIR = os.path.abspath('../static')

# mApp = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

mApp = Flask(__name__)

@mApp.route('/')
def Homepage():
    return render_template('Search.html')

@mApp.route('/Result',methods=['POST'])
def Result():
    mTextSearch = request.form['text']
    print(mTextSearch)
    try :
        mComparePrices = Prices(mTextSearch)
        mResult = mComparePrices.Result()
        mDataOut = {'Data': mResult}
        
        return render_template('Result.html', Result = mDataOut, TextSearch = mTextSearch)
    except:
        return 'No search results'

if __name__ == '__main__':
    mApp.run(debug=True)
