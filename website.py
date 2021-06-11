from flask import Flask, render_template, request
from ComparePrices import Prices
import os

mApp = Flask(__name__)

mWeb = ['Shopee', 'Tiki', 'Mediamart', 'Dien May Xanh', 'Lazada']


@mApp.route('/')
def Homepage():
    return render_template('Search.html', mSelected = [0, 1, 2, 3, 4], mWebSearch = mWeb)

@mApp.route('/Result',methods=['POST','GET'])
def Result():
    # mTextSearch = request.form['mTextSearch']
    mTextSearch = request.form.get("mTextSearch", False)
    selected = request.form.getlist('mWeb')
    selected = list(map(int, selected))
    try :        
        mComparePrices = Prices(mTextSearch)
        mData = mComparePrices.GetData()
    
        return render_template('Result.html', mResult = mData, TextSearch = mTextSearch, mSelected = selected, mWebSearch = mWeb)
    except:
        return 'No search results'

if __name__ == '__main__':
    mApp.run(debug=True)
