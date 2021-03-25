#import dependencies and libraries to be used
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

#scraping function that will be used by the route, data has to be stored in dictionaries
def scrape():
    # Splinter set up
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
                                
    #NASA SCRAPING

    #NASA URL to be scraped
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    html = browser.html

    #make beautiful soup object to be parsed with the html.parser
    news_soup = bs(html, 'html.parser')

    #use the find method to find all the instances of the specified class variable from the HTML of the page
    nasa_content_title = news_soup.find_all(class_='content_title')
    nasa_body_article = news_soup.find_all(class_='article_teaser_body')

    #initilizing lists for the for loop to hold the values
    news_title=[]
    news_paragraph = []

    #for loop to get the titles
    for title in nasa_content_title:
        try:
            news_title.append(title.a.text.strip())
        except:
            pass
    #for loop to get the body articles    
    for body in nasa_body_article:
        try:
            news_paragraph.append(body.text.strip())
        except:
            pass
        
    recent_news = news_title[0]
    recent_paragraph = news_paragraph[0]
    news_dict = {}
    news_dict['news title'] = recent_news
    news_dict['news paragraph'] = recent_paragraph

    #image scraping

    #amazon jpl url to be scraped
    featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'

    #open chrome and visit url
    browser.visit(featured_image_url)
    html = browser.html

    #make a beautifulsoup object so it can be parsed with the html.parser
    jpl_image_soup = bs(html, 'html.parser')

    #looking for the class in the html called headerimage
    featured_image = jpl_image_soup.find_all('img', class_='headerimage')

    #for loop to get the image
    for image in featured_image:
        featured_image_url = f"https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{image['src']}"
    jpl_image_dict = {}
    jpl_image_dict['img url'] = featured_image_url
    

    #Mars scrape

    # Scraped table containing facts about the planet
    mars_url = 'https://space-facts.com/mars/'

    # Read url and returned a list of DataFrames
    mars_table = pd.read_html(mars_url)
    mars_table = mars_table[1]

    # Converted data to HTML table string
    html_mars_table = mars_table.to_html()
    mars_dict = {}
    mars_dict['mars table'] = html_mars_table

    #hempishphere scrape

    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    #url that is being scraped
    browser.visit(hemispheres_url)
    html = browser.html

    #creating the beautifulsoup object
    soup = bs(html, 'html.parser')

    #finding all instanced of the class called description in the html
    names = soup.find_all(class_='description')

    #initlizing hemisphere_list
    hemisphere_list = []

    #for loop to ge the h3 anchor tags that are stored in the "names" variables
    for name in names:
        hemisphere_list.append(name.a.h3.text)

    #go through the pages to get the image info
    browser.visit(hemispheres_url)
    hemisphere_image_urls=[]
    for x in range(len(hemisphere_list)):
            html = browser.html
            soup = bs(html, 'html.parser')
            browser.click_link_by_partial_text(hemisphere_list[i])
            html = browser.html
            soup = bs(html, 'html.parser')
            title = hemisphere_list[i]
            img_url = soup.find(class_='downloads')
                
            hemisphere_dict = {}
            hemisphere_dict['title'] = title
            hemisphere_dict['img_url'] = img_url.a['href']
            hemisphere_image_urls.append(hemisphere_dict)
            browser.back()

    #Adding everything into dictionaries/lists
    nasa_data = []
    nasa_data.append(news_dict)
    nasa_data.append(jpl_image_dict)
    nasa_data.append(mars_dict)
    nasa_data.append(hemisphere_dict)

    #Close browser with splinter
    browser.quit()

    return nasa_data