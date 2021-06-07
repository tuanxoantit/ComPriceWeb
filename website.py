from flask import Flask, render_template, request
import os

from ComparePrices import Prices


mApp = Flask(__name__)

@mApp.route('/')
def Index():
    return render_template('Search.html')

@mApp.route('/Result',methods=['POST'])
def Result():
    mTextSearch = request.form['text']
    try :
        mComparePrices = Prices(mTextSearch)
        mResult = mComparePrices.Result()
        mDataOut = {'mData': mResult}
        
        return render_template('Result.html', mResultHtml = mDataOut, mTextSearchHtml = mTextSearch)
    except:
        return 'No search results'

if __name__ == '__main__':
    mApp.run(debug=True)
