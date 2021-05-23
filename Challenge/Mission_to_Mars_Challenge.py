#!/usr/bin/env python
# coding: utf-8

# In[661]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import re
import time
from webdriver_manager.chrome import ChromeDriverManager


# In[662]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[663]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[664]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[665]:


slide_elem.find('div', class_='content_title')


# In[666]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[667]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[668]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[669]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[670]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[671]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[672]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[673]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[674]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[675]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[676]:


# 1. Use browser to visit the URL 
hemisphere_url = 'https://marshemispheres.com/'

browser.visit(hemisphere_url)


# In[677]:


time.sleep(4)

# Assign the HTML content of the page to a variable
hemisphere_html = browser.html
# Parse HTML with Beautifulsoup
mars_soup = soup(hemisphere_html,'html.parser')


# In[678]:


# Collect the urls for the hemisphere images
items = mars_soup.find_all("div", class_="item")

main_url = "https://marshemispheres.com/"
hemisphere_urls = []

for item in items:
    hemisphere_urls.append(f"{main_url}{item.find('a', class_='itemLink')['href']}")

print(*hemisphere_urls, sep = "\n")


# In[679]:


# Create a list to store the data
hemisphere_image_urls=[]

# Loop through each url
for url in hemisphere_urls:
    # Navigate to the page
    browser.visit(url)
    
    time.sleep(4)
    
    # Assign the HTML content of the page to a variable
    hemisphere_html = browser.html
    # Parse HTML with Beautifulsoup
    mars_soup = soup(hemisphere_html,'html.parser')
    
    img_url = mars_soup.find('img', class_="wide-image")['src']
    title = mars_soup.find('h2', class_="title").text
    
    hemisphere_image_urls.append({"title":title,"img_url":f"https://marshemispheres.com/{img_url}"})


# In[680]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[681]:


# 5. Quit the browser
browser.quit()


# In[ ]:




