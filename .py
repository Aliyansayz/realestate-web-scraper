import requests
from bs4 import BeautifulSoup
import pandas as pd


class ZameenScrape:
  def __init__(self, url, pages_num ):
      self.url = url
      self.pages_num = pages_num

  def RequestPage(self, current_page , url):
    url = url.split('1.html')
    url = url[0]+f'{current_page}.html'

    page = requests.get(url)
    soup = BeautifulSoup(page.content , 'html.parser')
    return soup 

  def SelectData(self, soup):
    all_titles  = soup.find_all('a', class_='_7ac32433' )
    all_area  = soup.select("[aria-label='Area']")
    all_price = soup.select("[aria-label='Price']")
    return all_titles ,all_area , all_price

  def StoreData(self, all_titles ,all_area , all_price , current_page , title_list, area_list, price_list  ): 
    
    for name in all_titles:
      title_list.append(name.get('title'))

    for area in all_area:
      area_list.append(area.text)
  
    for price in all_price:
      price_list.append(price.text)
      
    return title_list ,  area_list , price_list

  def SaveCsv(self, title_list ,  area_list , price_list):
    df = pd.DataFrame({ "Name" : pd.Series(title_list) , "Area" : pd.Series(area_list) , "Price" : pd.Series(price_list) })
    df.to_csv(f'Propertydata'  , index=False)


  def DefineScrape(self, url, pages_num  ):
    title_list = []
    area_list = []
    price_list = []
    for i in range(1,pages_num+1):     
      current_page = i 
      soup = self.RequestPage(current_page , url)
      all_titles ,all_area , all_price = self.SelectData(soup)
      title_list ,  area_list , price_list = self.StoreData(all_titles ,all_area , all_price , current_page , title_list, area_list, price_list  )
      
    self.SaveCsv(title_list ,  area_list , price_list)

  def RunScrape(self):
     self.DefineScrape(self.url, self.pages_num)
      
