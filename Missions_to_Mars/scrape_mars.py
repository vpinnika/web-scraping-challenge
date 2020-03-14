# Dependencies
import pandas as pd
import requests as req
import time
from bs4 import BeautifulSoup as bs
from splinter import Browser
from pprint import pprint
import pymongo
from flask import Flask, render_template
import numpy as np
import json
from selenium import webdriver

def scrape():
    #Getting ChromeDriver path
    executable_path = {'executable_path': 'chromedriver.exe'}
    #Getting the browser
    browser = Browser('chrome', **executable_path, headless=False)

    #Defining an empty collection
    mars_collection = {}

    # Getting NASA Mars News
    url = ('https://mars.nasa.gov/news/')
    browser.visit(url)
    response = req.get(url)
    time.sleep(2)
    soup = bs(response.text, 'html.parser')
    
    mars_collection["news_title"] = soup.find('div', class_="content_title").get_text()
    mars_collection["news_snip"] = soup.find('div', class_="rollover_description_inner").get_text()
       
    
    #Getting Space Images
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    response = req.get(url)
    time.sleep(2)
    soup = bs(response.text, 'html.parser')    
    image_url = soup.find('article', class_='carousel_item')
    footer = image_url.find('footer')
    ref = footer.find('a')
    path = ref['data-fancybox-href']
    featured_image_url = ('https://www.jpl.nasa.gov' + path)

    mars_collection["featured_image_url"] = featured_image_url 
    
    #Getting Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    response = req.get(url)
    time.sleep(2)
    soup = bs(response.text, 'html.parser')
    contents = soup.find_all("div",class_="content")
    
    weather_mars = []
    for content in contents:
        tweet = content.find("div", class_="js-tweet-text-container").text
        weather_mars.append(tweet)
    mars_weather = weather_mars[8]
   
    mars_collection["mars_weather"] = mars_weather

    
    #Getting Mars Facts
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    table = pd.read_html(url)       
    df = table[0]
    df.columns = ["Facts", "Value"]
    facts_html = df.to_html()
    facts_html = facts_html.replace("\n","")
    mars_collection["fact_table"] = facts_html
    
    #Mars Hemispheres
    #Defining empty list
    hemisphere_image_urls =[]
  
    #Cerberus Hemisphere
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser.visit(url)
    response = req.get(url)
    time.sleep(2)
    soup = bs(response.text, 'html.parser')
    Cerberus_image = soup.find_all('div', class_="wide-image-wrapper")
    
    for img in Cerberus_image:
        pic = img.find('li')
        Cerberus_image_url = pic.find('a')['href']
    
    cerberus_title = soup.find('h2', class_='title').text   
    Cerberus_Hemisphere = {"Title": cerberus_title, "url": Cerberus_image_url}
    
    hemisphere_image_urls.append(Cerberus_Hemisphere)
    
    
    #Schiaparelli Hemisphere
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    browser.visit(url)
    response = req.get(url)
    time.sleep(2)
    soup = bs(response.text, 'html.parser')
    shiaparelli_img = soup.find_all('div', class_="wide-image-wrapper")
    
    for img in shiaparelli_img:
        pic = img.find('li')
        shiaparelli_img_url = pic.find('a')['href']
    
    shiaparelli_title = soup.find('h2', class_='title').text
    Schiaparelli_Hemisphere = {"Title": shiaparelli_title, "url": shiaparelli_img_url}
    
    hemisphere_image_urls.append(Schiaparelli_Hemisphere)
    
    
    #Syrtis Major Hemisphere
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    browser.visit(url)
    response = req.get(url)
    time.sleep(2)
    soup = bs(response.text, 'html.parser')
    syrtris_img = soup.find_all('div', class_="wide-image-wrapper")

    for img in syrtris_img:
        pic = img.find('li')
        syrtris_img_url = pic.find('a')['href']
    
    syrtris_title = soup.find('h2', class_='title').text
    Syrtis_Major_Hemisphere = {"Title": syrtris_title, "url": syrtris_img_url}
    
    hemisphere_image_urls.append(Syrtis_Major_Hemisphere)
    
    #Valles Marineris Hemisphere
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    browser.visit(url)
    response = req.get(url)
    time.sleep(2)
    soup = bs(response.text, 'html.parser')
    valles_marineris_img = soup.find_all('div', class_="wide-image-wrapper")
    
    for img in valles_marineris_img:
        pic = img.find('li')
        valles_marineris_img_url = pic.find('a')['href']
    
    valles_marineris_title = soup.find('h2', class_='title').text
    Valles_Marineris_Hemisphere = {"Title": valles_marineris_title, "url": valles_marineris_img_url}
    
    hemisphere_image_urls.append(Valles_Marineris_Hemisphere)
    
    mars_collection["hemisphere_image"] = hemisphere_image_urls    
    
    return mars_collection

if __name__ == "__main__":
    scrape()
    