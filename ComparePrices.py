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
        mPrices = [int(Price.contents[0].strip('\xa0₫').replace('.','')) for Price in mSpanPrices ]

        mDivStores = mSoup.find_all('div', {'class' : 'mqQL1e'})
        mStores = [Store.find_next('span').string for Store  in mDivStores] 

        mALinks = mSoup.find_all('a', {'class' : 'translate-content'})
        mLinks = [Link['href'] for Link in mALinks ]

        # print(mPrices)
        # print(mStores)
        # print(mLinks)
        return mPrices, mStores, mLinks
        
    def Result(self):
        mPrices, mStores, mLinks = self.GetData()
        mData = [[Price, Store, 'https://www.google.com{0}'.format(Link)] for Price,Store,Link in sorted(zip(mPrices,mStores,mLinks))]
        return mData


