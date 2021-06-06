from flask import Flask, render_template, request
from ComparePrices import Prices

mApp = Flask(__name__)

@mApp.route('/')
def Homepage():
    return render_template('Search.html')

@mApp.route('/',methods=['POST'])
def Result():
    mTextSearch = request.form['text']
    print(mTextSearch)
    try :
        mComparePrices = Prices(mTextSearch)
        mResult = mComparePrices.Result()
        mDataOut = {'Data': mResult}
        # mDataOut = {'Data':[[1,2,3],[4,5,6]]}
        return render_template('Result.html', Result = mDataOut)
    except:
        return 'Không có kết quả tìm kiếm'

if __name__ == '__main__':
    mApp.run(debug=True)
