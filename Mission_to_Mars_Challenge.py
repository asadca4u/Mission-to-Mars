#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# In[2]:


# Path to chromedriver
get_ipython().system('which chromedriver')


# In[3]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)


# ### Visit the NASA Mars News Site

# In[4]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[5]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[6]:


slide_elem.find("div", class_='content_title')


# In[7]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[8]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### JPL Space Images Featured Image

# In[9]:


# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[10]:


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# In[11]:


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# In[12]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[13]:


# find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# In[14]:


# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# ### Mars Facts

# In[15]:


df = pd.read_html('http://space-facts.com/mars/')[0]

df.head()


# In[16]:


df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df


# In[17]:


df.to_html()


# ### Mars Weather

# In[18]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[19]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[20]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[21]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[22]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for i in range(1,5): 

    #create empty dictonary to store scraped information
    hemispheres = {}

    #define xpath
    xpath = '/html/body/div[1]/div[1]/div[2]/section/div/div[2]'
    
    # Scrape the image title
    title = browser.find_by_xpath(f'{xpath}/div[{i}]/div/a/h3').value  
    title
    
    #Find image thumbnail and click it
    thumbnail = browser.find_by_xpath(f'{xpath}/div[{i}]/a/img')
    thumbnail.click()

    # Find the relative image url
    html = browser.html
    img_soup = soup(html, 'html.parser')
  
    # Find the relative image url
    img_url_rel = img_soup.select_one('img.wide-image').get("src")
    # Create the complete url to the image
    img_url = f'https://astrogeology.usgs.gov{img_url_rel}'
    
    # Add image url and image title to hemispheres dictionary 
    hemispheres.update({'img_url':img_url,'title':title})
    
    # Append the list to add dictionary
    hemisphere_image_urls.append(hemispheres)
    
    #return to previous page to begin next cycle of loop
    browser.visit(url)
    


# In[23]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[25]:


# 5. Quit the browser
browser.quit()
