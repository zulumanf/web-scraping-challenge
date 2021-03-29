from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

#scrape function
def scrape():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #NASA 

    #visit mars NASA url without paramters in URL
    MarsNews_url = 'https://mars.nasa.gov/news/'
    browser.visit(MarsNews_url)

    #create html object
    html = browser.html

    #create beatifulsoup object, parse html
    soup = bs(html, 'html.parser')

    #this contains the latest news title and paragraph text
    first_child = soup.find('li', class_='slide')

    #save under the <div> tag with a class of 'content_title', do not do find all
    news_title = first_child.find('div', class_='content_title').text
    print(news_title)

    #save the paragraph text under the <div> tag with a class of 'article_teaser_body', do not do find all
    news_para = first_child.find('div', class_='article_teaser_body').text
    print(news_para)

    #Scraping JPL Featured Image URL

    # JPL Website
    jpl_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'

    #visit jpl url
    browser.visit(jpl_url)

    html = browser.html

    #create beautiful soup object, parse
    j_soup = bs(html, 'html.parser')

    #look for image of class headerimage
    main_image = j_soup.find_all('img', class_='headerimage')
    for image in main_image:
        #f string to pull in the image url
        jpl_image_url = f"https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{image['src']}"

    #print the image url
    print(jpl_image_url)


    #Scraping Mars Facts¶


    #go to mars facts website
    marsfacts_url = 'https://space-facts.com/mars/'
    browser.visit(marsfacts_url)

    #create html object
    html = browser.html

    #read html with pandas
    mars_table = pd.read_html(html)

    #create pandas dataframe and slice it into the appropiate columns
    marsfacts_df = mars_table[0]
    marsfacts_df.columns =['Description', 'Value']
    marsfacts_df

    # Converted data to HTML table string
    html_mars_table = marsfacts_df.to_html()
    print(html_mars_table)

    #Mars Hemisphere


    #visit mars hemi url
    mars_hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemi_url)


    #create html object
    html = browser.html

    #create beautiful soup object, parse 
    soup = bs(html, 'html.parser')

    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(hemispheres_url)



    #get parent div
    hemi_divs = soup.find_all('div', class_="item")

    #initialize list
    hemisphere_image_data = []

    #loop through to get hemi data
    for hemisphere in range(len(hemi_divs)):

        hem_link = browser.find_by_css("a.product-item h3")
        hem_link[hemisphere].click()
        time.sleep(1)
        img_detail_html = browser.html
        imagesoup = BeautifulSoup(img_detail_html, 'html.parser')
    
        #base url
        base_url = 'https://astrogeology.usgs.gov'
    
        #image url, add base plus image url to create final url
        hem_url = imagesoup.find('img', class_="wide-image")['src']
        img_url = base_url + hem_url
        img_title = browser.find_by_css('.title').text
    
        hemisphere_image_data.append({"title": img_title,
                              "img_url": img_url})
    
        #go back to main page
        browser.back()
    
    #close the session    
    browser.quit()

    hemisphere_image_data



