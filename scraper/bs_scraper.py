from bs4 import BeautifulSoup
import requests


test_url = 'https://pedia.watcha.com/ko-KR/users/DgwxAeQYNxrMj/contents/movies/ratings'
response = requests.get(test_url)
if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    for movie_div in soup.find_all('li', class_='css-8y23cj'):
        title = movie_div.find('div', class_='css-niy0za').text
        rating = float(movie_div.find('div', class_='css-m9i0qw').text.split()[-1])
        print(title, rating)

else:
    raise ConnectionError(f"Error {response.status_code} occurred.")
