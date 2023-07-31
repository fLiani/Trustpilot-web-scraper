import sys
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

page_num = 1
reviews = []

while page_num <= int(sys.argv[2]):

    url = f'{sys.argv[1]}?languages=all&page={page_num}&sort=recency'

    response = requests.get(url)

    response = response.content

    soup = BeautifulSoup(response, 'html.parser')

    review = soup.findAll("section", class_='styles_reviewContentwrapper__zH_9M')

    for review in review:
        try:
            title = review.find("h2", class_='typography_heading-s__f7029 typography_appearance-default__AAY17').text
        except:
            title = ''
        try:
            description = review.find("p", class_='typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn').text
        except:
            description = ''
        try:
            rating_container = review.find("div", class_='styles_reviewHeader__iU9Px')
        except:
            print("NO RATING FOUND")
            break
        try:
            star_rating = rating_container.attrs['data-service-review-rating']
        except:
            print("NO STAR RATING")
            break
        reviews.append([title, description, star_rating])

    print(url)
    page_num += 1
    time.sleep(2)
    
df = pd.DataFrame(reviews, columns=['Title', 'Description', 'Star Rating'])

df.to_csv('reviews.csv')