import pandas as pd

from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Declare and intialize the final dictionary output
    final_dict_op = {}

    # NASA MARS News
    mars_url = "https://redplanetscience.com/"
    # visit the website
    browser.visit(mars_url)
    # get the HTML
    html = browser.html
    # setup bs4 to be used as html parser
    soup = bs(html, 'html.parser')
    # get all the titles for the latest news
    titles_latest = soup.find_all('div', class_='content_title')
    # Just get the latest of all the titles under the titles_latest
    news_title = titles_latest[0].text
    # Get the paragraph content under the above news title
    recent_news_paragraphs = soup.find_all('div', class_='article_teaser_body')
    news_paragraph = recent_news_paragraphs[0].text

    final_dict_op['title'] = news_title
    final_dict_op['news'] = news_paragraph

    # JPL MARS Space Images -- Featured Image

    pictures_url = 'https://spaceimages-mars.com/'
    browser.visit(pictures_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    featured_image_url_initial = soup.find_all(
        'img', class_='headerimage fade-in')
    # get the src part and apppend it to the pictures_url
    featured_image_url = f'{pictures_url}{featured_image_url_initial[0]["src"]}'

    final_dict_op['image_url'] = featured_image_url

    # MARS Facts
    mars_facts_url = 'https://galaxyfacts-mars.com/'
    browser.visit(mars_facts_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    # get the tables from the html as lists
    tables_as_lists = pd.read_html(mars_facts_url, header=0)
    mars_facts_df = tables_as_lists[0]
    html_table = mars_facts_df.to_html()
    html_table = html_table.replace('\n', '')

    final_dict_op['facts_table'] = html_table

    # MARS Hemispheres
    mars_hemispheres_url = 'https://marshemispheres.com/'
    browser.visit(mars_hemispheres_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    descriptions = soup.find_all('div', class_='description')

    hemisphere_images = soup.find_all('img', class_='thumb')
    image_urls = []
    for url in range(len(hemisphere_images)):
        image_urls.append(
            f'{mars_hemispheres_url}{hemisphere_images[url]["src"]}')
    hemisphere_names = []
    for des in range(len(descriptions)):
        hemisphere_names.append(descriptions[des].h3.text.strip())
    final_hemi_arr = []
    for index in range(len(hemisphere_names)):
        final_hemi_arr.append(
            {"title": hemisphere_names[index], "img_url": image_urls[index]})

    final_dict_op['hemisphere'] = final_hemi_arr

    # Quit the browser window
    browser.quit()

    # return final dictionary
    return final_dict_op
