def scrape_info():

    ## Dependencies
    from bs4 import BeautifulSoup as bs
    from splinter import Browser
    import pandas as pd
    import time

    ## Save urls
    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    facts_url = 'https://space-facts.com/mars/'
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


    ## NASA Mars News
    #### Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
        #### Assign the text to variables called news_title and news_p that you can reference later.

    # Open chrome browser
    executable_path = {'executable_path':'chromedriver.exe'}
    browser = Browser('chrome',**executable_path,headless=False, incognito=True)

    # Visit specified url
    browser.visit(news_url)

    # Save html from browser in object
    html = browser.html

    # Pass HTML string to bs
    news_html = bs(html,'html.parser')

    # Close chrome browser
    browser.quit()

    # Collect information for the latest news article
    latest_article = news_html.find('li',class_="slide")

    # Collect the lastest news title
    news_title = latest_article.find('div',class_="content_title").text

    # Collect the lastest news paragraph text
    news_p = latest_article.find('div',class_="article_teaser_body").text


    ## JPL Mars Space Images - Featured Image
    #### Visit the url for JPL Featured Space Image. Use splinter to navigate the site and find the image url for the current Featured Mars Image 
        #### and assign the url string to a variable called featured_image_url. Make sure to find the image url to the full size .jpg image. 
        #### Make sure to save a complete url string for this image.

    # Open chrome browser
    executable_path = {'executable_path':'chromedriver.exe'}
    browser = Browser('chrome',**executable_path,headless=False, incognito=True)

    # Visit specified url
    browser.visit(image_url)

    # Save html from browser in object
    html = browser.html

    # Pass HTML string to bs
    image_html = bs(html,'html.parser')

    # Close chrome browser
    browser.quit()

    # Collect the featured image href
    featured_image_href = image_html.find('a',id="full_image")['data-fancybox-href']

    # Save the complete featured image url
    featured_image_url = f"https://www.jpl.nasa.gov{featured_image_href}"


    ## Mars Weather
    #### Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. 
        #### Save the tweet text for the weather report as a variable called mars_weather.

    # Open chrome browser
    executable_path = {'executable_path':'chromedriver.exe'}
    browser = Browser('chrome',**executable_path,headless=False, incognito=True)

    # Visit specified url
    browser.visit(weather_url)

    # Save html from browser in object
    html = browser.html

    # Pass HTML string to bs
    weather_html = bs(html,'html.parser')

    # Close chrome browser
    browser.quit()

    # Collect the latest Mars weather tweet
    mars_weather = weather_html.find('p',class_="tweet-text").contents[0]


    ## Mars Facts
    #### Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc. 
        #### Use Pandas to convert the data to a HTML table string.

    # Scrape the Mars facts table and save as a df
    mars_facts_df = pd.read_html(facts_url)[0]

    # Specify column names
    mars_facts_df.columns =['Description','Value'] 

    # Convert and save Pandas df to HTML table
    mars_facts = mars_facts_df.to_html(index=False,justify='left',classes='table table-striped table-bordered')


    ## Mars Hemispheres
    #### Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres. You will need to click each of the links 
        #### to the hemispheres in order to find the image url to the full resolution image. Save both the image url string for the full resolution hemisphere image, 
        #### and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title. 
        #### Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

    # Create list of hemisphere names
    hemispheres_list = ['Cerberus Hemisphere Enhanced',
                      'Schiaparelli Hemisphere Enhanced',
                      'Syrtis Major Hemisphere Enhanced',
                      'Valles Marineris Hemisphere Enhanced']

    # Create empty list for hemisphere names and urls
    hemispheres_name_url = []

    # Open chrome browser
    executable_path = {'executable_path':'chromedriver.exe'}
    browser = Browser('chrome',**executable_path,headless=False, incognito=True)

    # Visit specified url
    browser.visit(hemispheres_url)

    # Loop to save the hemisphere image urls
    for hemisphere in hemispheres_list:

        # Navigate to hemisphere image
        browser.click_link_by_partial_text(hemisphere)

        # Save html from browser in object
        html = browser.html

        # Pass HTML string to bs
        hemisphere_html = bs(html,'html.parser')

        # Collect and save hemisphere name
        hemisphere_name = hemisphere_html.find('h2',class_="title").text
        
        # Collect and save image url
        hemisphere_image_src = hemisphere_html.find('img',class_="wide-image")['src']
        hemisphere_image_url = f'https://astrogeology.usgs.gov{hemisphere_image_src}' 
       
        # Save url and name in dictionary
        hemisphere_dict = {"title":hemisphere_name, "img_url":hemisphere_image_url}
        
        # Add dictionary to list created above
        hemispheres_name_url.append(dict(hemisphere_dict))
        
        # Move back through browsing history to return to main page
        browser.back()
            
    # Close chrome browser
    browser.quit()
    
    ## Save scrape output in dictionary
    scrape_data = {"news_title":news_title,
                 "news_p":news_p,
                 "featured_image_url":featured_image_url,
                 "mars_weather":mars_weather,
                 "mars_facts":mars_facts,
                 "hemispheres_name_url":hemispheres_name_url}
                 
    ## Return results
    return scrape_data
