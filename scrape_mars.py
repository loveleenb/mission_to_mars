
# coding: utf-8

# ## NASA Mars News

# In[1]:


#import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd

def init_browser():
        #pointing to chromedriver path
        executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
        return Browser("chrome", **executable_path, headless=False)

def scrape():
        browser = init_browser()
        
        # create surf_data dict that we can insert into mongo
        mars_data = {}

        #visiting the url using splinter
        url = "https://mars.nasa.gov/news/"
        browser.visit(url)

        # HTML Object
        html = browser.html
        # Parse HTML with Beautiful Soup
        soup = bs(html,"lxml")

        # Retrieve the latest element that contains news title and news_paragraph
        news_title = soup.find("div",class_="content_title").text
        news_p = soup.find("div", class_="article_teaser_body").text

        mars_data['news_title'] = news_title
        mars_data['news_paragraph'] = news_p


        # ## JPL Mars Space Images - Featured Image

        # Visit Mars Space Images through splinter module
        image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        browser.visit(image_url)

        # HTML Object
        html_img = browser.html
        # Parse HTML with Beautiful Soup
        soup = bs(html_img,"lxml")
        # Retrieve background-image url
        featured_image = soup.find('article')['style'].replace("background-image: url('", "").replace("');", "")
        base_url = "https://www.jpl.nasa.gov"
        featured_image_url = base_url + featured_image
        featured_image_url
        mars_data['featured_image_url'] = featured_image_url


        # ## Mars Weather

        # Visit Mars Weather Twitter through splinter module
        weather_url = "https://twitter.com/marswxreport?lang=en"
        browser.visit(weather_url)

        # HTML Object
        html_weather = browser.html
        # Parse HTML with Beautiful Soup
        soup = bs(html_weather,"lxml")

        # Find all elements that contain tweets
        weather_tweet = soup.find_all("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")

        # Loop through tweets to find latest weather tweet
        for tweet in weather_tweet:
                tweet = tweet.text
                if 'winds' and 'mph' in tweet:
                        mars_tweet = tweet
                        break
        return mars_tweet
             
        mars_data['mars_tweet'] = mars_tweet   

        # ## Mars Facts

        # Mars facts url 
        facts_url = "http://space-facts.com/mars/"

        # Use Panda's `read_html` to parse the url
        facts_df = pd.read_html(facts_url) 
        # Find the mars facts DataFrame in the list of DataFrames
        facts_df = facts_df[0]
        # Assign the columns `['Description', 'Value']`
        facts_df.columns = ["Description", "Value"]
        facts_df.set_index("Description", inplace=True)
        facts_df
        mars_data['mars_facts'] = facts_df


        # ## Mars Hemispheres

        # Visit hemispheres url
        hem_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        # HTML Object
        browser.visit(hem_url)
        html_hem = browser.html
        soup = bs(html_hem,"lxml")

        # Retreive all items that contain mars hemispheres information
        links = soup.find_all("div", class_ = 'item')

        # Create empty list for hemisphere urls 
        hem_image_urls = []

        # base url
        base_url = "https://astrogeology.usgs.gov"

        # Loop through the items previously stored
        for link in links:
                # Store title
                title = link.find('h3').text
                # Find title link url
                title_link = link.find("a")["href"]

                tile_link = base_url + title_link
                
                # Visit title url
                browser.visit(tile_link)
                html_img = browser.html
                soup = bs(html_img,"lxml")
                
                # Get full image url
                full_image = soup.find("img", class_ = "wide-image")["src"]
                full_image_url = base_url + full_image
                
                # Append the retreived information into a list of dictionaries 
                hem_image_urls.append({"title" : title, "img_url" : full_image_url})
                
                # Go back to hemispheres url to get next title
                hem_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
                browser.visit(hem_url)

        # return our mars data dict        
        mars_data['hem_image_urls'] = hem_image_urls

        return mars_data
        browser.quit()
        


