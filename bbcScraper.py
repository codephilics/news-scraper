import requests
from bs4 import BeautifulSoup

root_url = 'https://www.bbc.com'
response = requests.get(root_url + "/news")
doc = BeautifulSoup(response.text, 'html.parser')


def find_bbc_article(url):
    print(url)
    response_article = requests.get(url)
    soup = BeautifulSoup(response_article.text, 'html.parser')

    body = soup.find(property="articleBody")
    description = [p.text for p in body.find_all("p")]
    if description:
        description = '\n'.join(description)

    try:
        img_url = soup.find('img', {'class': "js-image-replace"}).get('src')
        # if imgUrl:
        #    print(imgUrl)
    except:
        print("No Image")
    # imgUrl = 'test'

    time = soup.find(class_="date").attrs['data-seconds']

    # if time:
    #    print(time)
    # time = "fdsdf"
    return description, img_url, time


def bbc_scraper():
    stories_list = []
    stories = doc.find_all('div', {'class': 'gs-c-promo'})
    for story in stories:
        headline = story.find('h3')
        link = story.find('a')

        article_url = root_url + link['href']

        try:
            description, imgUrl, time = find_bbc_article(article_url)

            '''
            story_dict = {
                'headline'    : headline.text,
                'description' : description,
                'url'         : articleUrl,
                'urlToImage'  : imgUrl,
                'publishedAt' : time
            } 
            '''

            story_dict = {
                             "source": {
                                 "id": link['href'],
                                 "name": "BBC"
                             },
                             "author": "Null",
                             "title": headline.text,
                             "description": description,
                             "url": article_url,
                             "urlToImage": imgUrl,
                             "publishedAt": time
                         },

            # Add the dict to our list
            stories_list.append(story_dict)

        except:
            print("Url error")

    print(stories_list)


bbc_scraper()
