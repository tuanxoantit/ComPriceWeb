from bs4 import BeautifulSoup
import requests

class Prices():
    mHeaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    def __init__(self, mProduct):
        self.mProduct = mProduct
        self.mUrl ='https://www.google.com/search?q={0}&tbm=shop'.format(self.mProduct )  
        # self.mUrl = 'https://www.google.com/search?q=card+man+hinh&tbm=shop' 
    
    def GetData(self):  
        mRes = requests.get(self.mUrl, headers = self.mHeaders)
        mSoup = BeautifulSoup(mRes.text,'html.parser')

        mSpanPrices = mSoup.find_all('span', {'class' : 'a8Pemb'})
        mStrPrices = [mPrice.contents[0] for mPrice in mSpanPrices ]
        mPrices = [int(mPrice.contents[0].strip('\xa0₫').replace('.','')) for mPrice in mSpanPrices ]

        mDivStores = mSoup.find_all('div', {'class' : 'mqQL1e'})
        mStores = [mStore.find_next('span').string for mStore  in mDivStores] 

        mALinks = mSoup.find_all('a', {'class' : 'translate-content'})
        mLinks = [mLink['href'] for mLink in mALinks ]

        # print(mPrices)
        # print(mStores)
        # print(mLinks)
        return mPrices, mStrPrices, mStores, mLinks
        
    def Result(self):
        mPrices, mStrPrices, mStores, mLinks = self.GetData()
        mData = [[StrPrices, Store, 'https://www.google.com{0}'.format(Link)] for Price, StrPrices, Store, Link in sorted(zip(mPrices, mStrPrices, mStores, mLinks))]
        return mData


