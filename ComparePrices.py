import requests
import json

class Prices():
    mHeaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    def __init__(self, mProduct):
        self.mProduct = mProduct
        self.mUrl ='https://shopee.vn/api/v4/search/search_items?by=relevancy&keyword={0}&limit=10&newest=0&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2'.format(self.mProduct)
        self.mUrlShopee = 'https://shopee.vn/api/v4/search/search_items?by=relevancy&keyword={0}&limit=10&newest=0&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2'.format(self.mProduct)
        self.mUrlLazada= 'https://www.lazada.vn/catalog/?q=={0}'.format(self.mProduct )
        self.mUrlTiki = 'https://tiki.vn/api/v2/products?limit=10&include=advertisement&aggregations=1&trackity_id=5e241048-5c36-3899-05d6-d9c8af97c3ac&q={0}'.format(self.mProduct )

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

    def ThousandsSeparator(self, mInput):
        mData = '{:20,.0f}'.format(mInput) + " VND"
        return mData

    def GetData(self):
        mShopeeData = self.Shopee()
        mTikiData = self.Tiki()
        mData = mShopeeData + mTikiData
        mData = sorted(mData, key=lambda l:l[1])
        mData = [{'Name': mData[0] ,'Price': mData[2], 'Link' : mData[3], 'Store': mData[4]} for mData in mData]
        return mData


# mPrice = Prices('book')
# mPrice.Shopee()
# mPrice.GetData()
# mPrice.ThousandsSeparator(100000000000000)
