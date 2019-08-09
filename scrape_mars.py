
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
# Mars News Code
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    slides = soup.find_all('div', class_='list_text')
    titles = []
    paragraphs = []
    for slide in slides:
        title = slide.find('div', class_='content_title')
        paragraph = slide.find('div', class_='article_teaser_body')
        titles.append(title)
        paragraphs.append(paragraph)
    title_code = str(titles[0])
    titlesplit = title_code.split('>')[2]

    # title1 is the final title variable
    title1 = titlesplit.split('<')[0]
    para_code = str(paragraphs[0])
    parasplit = para_code.split('>')[1]
    # para1 is the final paragraph variable
    para1 = parasplit.split('<')[0]


    # Mars Images Code

    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')
    featured_img = soup2.find('article', class_='carousel_item')
    fi_url = str(featured_img)
    split3 = fi_url.split('url(')[1]
    split4 = split3.split(')')[0]
    img_url = split4[1:-1]
    # featured_image_url is the final variable
    featured_image_url = 'https://www.jpl.nasa.gov' + img_url


    # Mars Weather Code

    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    html3 = browser.html
    soup3 = BeautifulSoup(html3, 'html.parser')
    # This pulls all tweets
    tweets = soup3.find_all('div', class_="js-tweet-text-container")
    # Create a blank list to store tweets
    tweet_text = []
    # This key phrase is in all desired tweets
    key = 'InSight sol'

    # Find the desired tweets, add them to the list
    for tweet in tweets:
        if key in str(tweet):
            tweet_text.append(tweet)
    # Identify the most recent tweet        
    most_recent = str(tweet_text[0])

    # Clean up the text
    weathersplit = str(most_recent.split('lang="en">InSight ')[1])

    mars_weather = weathersplit.split('<a')[0]


    # Mars Fact Code
    url4 = 'https://space-facts.com/mars/'

    tables = pd.read_html(url4)
    df = tables[1]
    df.columns = ['MARS PLANET PROFILE', '']
    # df.set_index = ['']
    df.set_index('MARS PLANET PROFILE', inplace=True)
    df.to_html('mars_facts.html', justify='left')
    fname = 'mars_facts.html'
    html_file = open(fname, 'r')
    mars_facts = html_file.read() 

    # Mars Hemispheres Code
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5)

    html5 = browser.html
    soup5 = BeautifulSoup(html5, 'html.parser')
    items = soup5.find_all('div', class_='item')
    hemisphere_image_urls = []
    for item in items:
        href = str(item.find('a', class_='itemLink product-item'))
        splithref = href.split('map')[1]
        hemihref = 'https://astropedia.astrogeology.usgs.gov/download' + splithref.split('">')[0] + '.tif/full.jpg'
        namefull = str(item.find('h3'))
        name = namefull[4:-14]
        hemisphere_image_urls.append({'title': name, 'img_url': hemihref})

    mars_data = {
        "first_headline": title1, "first_para": para1, "featured_img": featured_image_url, "mars_weather": mars_weather,\
        "mars_facts": mars_facts, "hemispheres": hemisphere_image_urls
    }
    browser.quit()

    return(mars_data)


