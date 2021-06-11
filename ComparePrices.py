import requests
import json
from bs4 import BeautifulSoup
import urllib3


class Prices():
    mHeaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    mLitmit = 10
    def __init__(self, mProduct):
        self.mProduct = mProduct
        self.mUrl ='https://shopee.vn/api/v4/search/search_items?by=relevancy&keyword={0}&limit=10&newest=0&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2'.format(self.mProduct)
        self.mUrlShopee = 'https://shopee.vn/api/v4/search/search_items?by=relevancy&keyword={0}&limit={1}&newest=0&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2'.format(self.mProduct, self.mLitmit)
        self.mUrlLazada= 'https://www.lazada.vn/catalog/?q={0}&_keyori=ss&from=input&spm=a2o4n.home.search.go.1905e182rXSi4S'.format(self.mProduct )
        self.mUrlTiki = 'https://tiki.vn/api/v2/products?limit={0}&include=advertisement&aggregations=1&trackity_id=5e241048-5c36-3899-05d6-d9c8af97c3ac&q={1}'.format(self.mLitmit, self.mProduct )
        self.mUrlMediamart = 'https://mediamart.vn/tim-kiem?kw={0}'.format(self.mProduct)
        
        mProductDMX = mProduct.replace(' ','-')
        self.mUrlDienmayxanh = 'https://www.dienmayxanh.com/{0}'.format(mProductDMX)

    def Shopee(self):  
        mData = json.loads(requests.get(self.mUrlShopee, headers = self.mHeaders).text)
        # mProducts = [[mProduct['item_basic']['name'], mProduct['item_basic']['price'], f'https://shopee.vn/a-i.{mProduct["shopid"]}.{mProduct["itemid"]}'] for mProduct in mData['items']]
        mProducts = []
        for mProduct in mData['items']:
            mName = mProduct['item_basic']['name']
            mPrice = int(str(mProduct['item_basic']['price'])[:-5])
            mStrPrice = self.ThousandsSeparator(mPrice)
            mLink = f'https://shopee.vn/a-i.{mProduct["shopid"]}.{mProduct["itemid"]}'
            mDictProduct = [mName, mPrice, mStrPrice, mLink, "Shopee"]
            mProducts.append(mDictProduct)
        return mProducts    

    def Tiki(self):
        mRawData = requests.get(self.mUrlTiki, headers = self.mHeaders).text
        mData = json.loads(requests.get(self.mUrlTiki, headers = self.mHeaders).text)
        # mProducts = [[mProduct['name'], mProduct['price'], f'https://tiki.vn/{mProduct["url_path"]}'] for mProduct in mData['data']]
        mProducts = []
        for mProduct in mData['data']:
            mName = mProduct['name']
            mPrice = int(mProduct['price'])
            mStrPrice = self.ThousandsSeparator(mPrice)
            mLink = f'https://tiki.vn/{mProduct["url_path"]}'
            mDictProduct = [mName, mPrice, mStrPrice, mLink, 'Tiki']
            mProducts.append(mDictProduct)
        return mProducts

    def Lazada(self):
        print("Lazada : ", self.mUrlLazada)
        mRawData = requests.get(self.mUrlLazada, headers = self.mHeaders).text
        # mData = json.loads(requests.get(self.mUrlLazada, headers = self.mHeaders).text)
        print(mRawData)
        # mProducts = [[mProduct['name'], mProduct['price'], f'https://tiki.vn/{mProduct["url_path"]}'] for mProduct in mData['data']]
        # mProducts = []
        # for mProduct in mData['data']:
        #     mName = mProduct['name']
        #     mPrice = int(mProduct['price'])
        #     mStrPrice = self.ThousandsSeparator(mPrice)
        #     mLink = f'https://tiki.vn/{mProduct["url_path"]}'
        #     mDictProduct = [mName, mPrice, mStrPrice, mLink, 'Tiki']
        #     mProducts.append(mDictProduct)
        # return mProducts

    def Mediamart(self):
        print("Lazada : ", self.mUrlMediamart) 
        mRes = requests.get(self.mUrlMediamart, headers = self.mHeaders)
        mSoup = BeautifulSoup(mRes.text,'html.parser')

        mProducts = []
        for mIndex in range(self.mLitmit):
            try :
                mClass = self.GetClassMediamart(mIndex)
                mLiPrices = mSoup.find_all('li', {'class' : mClass})
                mDataPrice = mLiPrices[0].find_all('div', {'class' : 'pl18-item-pbuy'})
                mStrPrice = mDataPrice[0].text.strip()
                mPrice = int(mStrPrice.replace('.','').strip('đ'))
                mDataLink = mLiPrices[0].find_all('a', href=True)
                mLink = 'https://mediamart.vn/' + mDataLink[0]['href']
                mName = mDataLink[0]['title']
                mDictProduct = [mName, mPrice, mStrPrice, mLink, 'Mediamart']
                mProducts.append(mDictProduct)
            except:
                print(mIndex)
        return mProducts

    def GetClassMediamart(self, mIndex):
        if mIndex < 2 :
            mClass = 'pl18-item-li pl18-item-li-{0} pl18-item-li-big pl18-item-li-mover'.format(mIndex)
        else :
            mClass = 'pl18-item-li pl18-item-li-{0} pl18-item-li-mover'.format(mIndex)
        return mClass
        
    def Dienmayxanh(self):
        print("Dienmayxanh : ", self.mUrlDienmayxanh) 
        mRes = requests.get(self.mUrlDienmayxanh, headers = self.mHeaders)
        mSoup = BeautifulSoup(mRes.text,'html.parser')

        mProducts=[]
        mLiData = mSoup.find_all('li', {'class' : 'item'})
        mIndex = 0
        for mData in mLiData:
            mDataPrice = mData.find_all('strong', {'class' : 'price'})
            mStrPrice = mDataPrice[0].text.strip()
            mPrice = int(mStrPrice.replace('.','').strip('₫'))
            mDataLink = mData.find_all('a', href=True)
            mLink = 'https://www.dienmayxanh.com' + mDataLink[0]['href']
            mName = mData.find('h3').text.strip()
            mDictProduct = [mName, mPrice, mStrPrice, mLink, 'DienMayXanh']
            mProducts.append(mDictProduct)
            mIndex += 1
            if mIndex >self.mLitmit:
                break
        return mProducts
    
    def WriteData(self, mSoup):
        with open("HTML.html", "w") as mFile:
            mFile.write(str(mSoup))
    
    def WriteDataCom(self, mSoup):
        mFile = open('DataHtml.html','a')
        mFile.write(mSoup)
        mFile.close()

    def ThousandsSeparator(self, mInput):
        mData = '{:20,.0f}'.format(mInput) + "đ"
        return mData

    def GetData(self):
        mShopeeData = self.Shopee()
        mTikiData = self.Tiki()
        mMediamartData = self.Mediamart()
        mDienmayxanh = self.Dienmayxanh()
        mData = mShopeeData + mTikiData + mMediamartData + mDienmayxanh
        mData = sorted(mData, key=lambda l:l[1])
        mData = [{'Name': mData[0] ,'Price': mData[2], 'Link' : mData[3], 'Store': mData[4]} for mData in mData]
        return mData


# mPrice = Prices('tivi')
# mPrice.Shopee()
# mPrice.Lazada()
# mPrice.Mediamart()
# mPrice.ThousandsSeparator(100000000000000)
# mPrice.GetData()
# mPrice.Dienmayxanh()

