import time
import pickle

from bs4 import BeautifulSoup
from selenium import webdriver


def get_whole_html_source(url, t_pause=0.5, max_scroll_count=float('inf')):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(1)
    last_height = driver.execute_script("return document.body.scrollHeight")

    scroll_count = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(t_pause)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break

        scroll_count += 1
        if scroll_count >= max_scroll_count:
            break

    page_source = driver.page_source
    driver.quit()
    return page_source


def get_ratings_from_html(html_source):
    mv_rating_dict = {}
    soup = BeautifulSoup(html_source, 'lxml')

    for movie_div in soup.find_all('li', class_='css-8y23cj'):
        title = movie_div.find('div', class_='css-niy0za').text
        rating = float(movie_div.find('div', class_='css-m9i0qw').text.split()[-1])
        mv_rating_dict[title] = rating

    return mv_rating_dict


def dump_dict_as_pkl(out_dict, save_path):
    with open(save_path, 'wb') as f:
        pickle.dump(out_dict, f)


if __name__ == '__main__':
    WATCHA_URL = 'https://pedia.watcha.com/ko-KR/users/DgwxAeQYNxrMj/contents/movies/ratings'
    SAVE_PATH = 'DONGJYN_MOVIES.pickle'

    html_source = get_whole_html_source(WATCHA_URL, max_scroll_count=3)
    mv_rating_dict = get_ratings_from_html(html_source)
    dump_dict_as_pkl(mv_rating_dict, SAVE_PATH)
