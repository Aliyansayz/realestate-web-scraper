import requests
from bs4 import BeautifulSoup
import pandas as pd


"""
HouseScraper = ZameenScrape('https://www.zameen.com/Homes/Lahore-1-1.html' , 5)
HouseScraper.RunScrape()

area_urls = ['https://www.zameen.com/Homes/Lahore-1-1.html', 'https://www.zameen.com/Homes/Lahore_Bahria_Town-509-1.html'
             'https://www.zameen.com/Homes/Lahore_Johar_Town-93-1.html', 'https://www.zameen.com/Homes/Lahore_Defence_(DHA)_Phase_3-1454-1.html']
LahoreHouseScraper = ZameenScrape(area_urls , 50)

LahoreHouseScraper.RunScrapeList()
"""
class ZameenScrape:
  def __init__(self, url, pages_num ):
      self.url = url
      self.pages_num = pages_num

  def RequestPage(self, current_page , url):
    url = url.split('1.html')
    z = url[0].split('/')
    area_name = z[4].split('-1')
    property_type =z[3]
    area_name = area_name[0].split('-')
    area_name = area_name[0]
    area_name , property_type
    url = url[0]+f'{current_page}.html'

    page = requests.get(url)
    soup = BeautifulSoup(page.content , 'html.parser')
    return soup , area_name , property_type

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

  def SaveCsv(self, title_list ,  area_list , price_list , area_name , property_type):
    df = pd.DataFrame({ "Name" : pd.Series(title_list) , "Area" : pd.Series(area_list) , "Price" : pd.Series(price_list) })
    df.to_csv(f'{area_name}_{property_type}'  , index=False)


  def DefineScrape(self, url, pages_num  ):
    title_list = []
    area_list = []
    price_list = []
    for i in range(1,pages_num+1):     
      current_page = i 
      soup , area_name , property_type = self.RequestPage(current_page , url)
      all_titles ,all_area , all_price = self.SelectData(soup)
      title_list ,  area_list , price_list = self.StoreData(all_titles ,all_area , all_price , current_page , title_list, area_list, price_list  )
      
    self.SaveCsv(title_list ,  area_list , price_list , area_name , property_type)

  def RunScrape(self):
     self.DefineScrape(self.url, self.pages_num)
      
  def RunScrapeList(self):
     for value in self.url:      
       self.DefineScrape(value, self.pages_num)

