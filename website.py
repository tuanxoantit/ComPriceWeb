from flask import Flask, render_template, request
from ComparePrices import Prices
import os

mApp = Flask(__name__)

@mApp.route('/')
def Homepage():
    return render_template('Search.html')

@mApp.route('/Result',methods=['POST','GET'])
def Result():
    # mTextSearch = request.form['mTextSearch']
    mTextSearch = request.form.get("mTextSearch", False)
    try :        
        mComparePrices = Prices(mTextSearch)
        mData = mComparePrices.GetData()
    
        return render_template('Result.html', mResult = mData, TextSearch = mTextSearch)
    except:
        return 'No search results'


if __name__ == '__main__':
    mApp.run(debug=True)
