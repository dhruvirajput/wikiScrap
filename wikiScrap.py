import os
import traceback
import logging

import bs4
import requests

from time import sleep
from log_main import initialize_logger


initialize_logger("wikiScrap")
module_directory = os.path.dirname(__file__)
base_url = "https://en.wikipedia.org/wiki/Special:Random"


def get_body_content(html_text):
    try:
        soup = bs4.BeautifulSoup(str(html_text), "html.parser")
        body_content = soup.find(id="mw-content-text").find(class_="mw-parser-output")

        body_content_soup = bs4.BeautifulSoup(str(body_content), "html.parser")
        clean_body_content = " ".join(str(p.text) for p in body_content_soup.find_all('p'))
        return clean_body_content

    except Exception as e:
        traceback.print_exc()
        logging.error("Failed to get the body content. Error: %s", e)
        return False


def run_scrapping():
    logging.info("Starting the scrapping process...")
    try:
        search_history = []
        for i in range(2000):

            response = requests.get(base_url)
            if str(response.url) not in search_history:
                search_history.append(response.url)

                f = open(module_directory + "/DataSet/" + str(i) + ".txt", "w")
                f.write(get_body_content(response.text))

                f_ = open(module_directory + "/DataSet/url_list.txt", "w")
                f_.write("\n".join(search_history))

            sleep(2)

        return True

    except Exception as e:
        traceback.print_exc()
        logging.error("Error: %s", e)
        print("Error: %s", e)
        return False


run_scrapping()
