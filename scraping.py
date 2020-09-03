# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

#function to initialize the browser, create a data dictionary, end the WebDriver and return the scraped data
def scrape_all():
   # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    #This line of code tells Python that we'll be using our mars_news function to pull this data
    news_title, news_paragraph = mars_news(browser)
    hemisphere_image_urls = mars_hemispheres(browser)

   # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "mars_hemispheres": hemisphere_image_urls
    }
 # Stop webdriver and return data
    browser.quit()
    return data

#function to scrape the news title and paragraph summary
def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

#function to scrape the featured image
def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')[0]
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

#function to scrape mars facts
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")


def mars_hemispheres(browser):
    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

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

    return hemisphere_image_urls


#This last block of code tells Flask that our script is complete and ready for action
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())