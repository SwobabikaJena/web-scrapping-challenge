from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    # Define path to the chromedriver
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # Visit url of NASA Mars News Site and open in browser
    url_nasa = "https://mars.nasa.gov/news/"
    browser.visit(url_nasa)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the first instance of the target 
    results = soup.select_one("ul.item_list li.slide")

    # Identify and return the Latest News
    title = results.find("div", class_="content_title").text

    # Identify and return corresponding Paragraph Text 
    para_text = results.find("div", class_="article_teaser_body").text
 


    # Visit url of JPL Featured Space Image page and open in browser
    url_spaceImg = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url_spaceImg)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Get the image url from soup
    featured = soup.find('img', class_='headerimage fade-in')
    featured_image = featured['src']
    featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + featured_image



    # Visit url of  Mars Facts webpage and open in browser
    url_spaceFacts = 'https://space-facts.com/mars/'
    browser.visit(url_spaceFacts)

    # Use Panda's `read_html` to parse the url and get the tables
    tables = pd.read_html(url_spaceFacts)

    # Find table containing facts about the planet including Diameter, Mass, etc. 
    df_marsFacts = tables[2]
    df_marsFacts.columns = ['Features', 'Mars']
    marsFacts_table = df_marsFacts.to_html(classes="table table-striped")
    marsFacts_table.replace('\n','')



    # Visit url of USGS Astrogeology site and open in browser
    base_url = 'https://astrogeology.usgs.gov/'
    url_marsHS = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_marsHS)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Identify and return the data path
    all_hems = soup.find('div', class_ = 'collapsible results')
    hems = soup.find_all('div', class_='item')

    # Get the image url and titles from soup
    hemisphere_image_urls = []
    for hem in hems:
        try:
            hem_data = hem.find('div', class_='description')  
            hem_title = hem_data.a.h3.text

            # Get full image link url and scrape data
            hemPic_url = hem_data.a['href']
            browser.visit(base_url+hemPic_url)
    
            # Scrape page into Soup
            html = browser.html
            img_soup = bs(html, 'html.parser')

            # Identify and return the data path
            img_src1=img_soup.find('div', class_='downloads')
            img_src = img_src1.find('li').a['href']

            # Populate data in a dictionary
            hem_dict={
                'hem_title':hem_title,
                'image_url':img_src
            }

            # Update list after each data retrieval
            hemisphere_image_urls.append(hem_dict)
        except Exception as e:
            print(e) 


    # Store data in a dictionary
    mars_dictionary = {
        "news_title": title,
        "news_paragraph": para_text,
        "featured_image_url" : featured_image_url,
        "marsFacts_table" : marsFacts_table,
        "hemispheres" : hemisphere_image_urls
    }

    # Quit the browser after scraping
    browser.quit()
    print(mars_dictionary)

    # Return results
    return mars_dictionary

if __name__ == "__main__":
    scrape()