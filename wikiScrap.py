import os
import traceback
import logging

import bs4
import requests

from time import sleep
from log_main import initialize_logger


# Initialize the logging file with parameter as the name of the file.
initialize_logger("wikiScrap")
# this store the location path from the root to the module folder.
module_directory = os.path.dirname(__file__)
# the wikipedia url which redirects to the random post.
base_url = "https://en.wikipedia.org/wiki/Special:Random"


def get_body_content(html_text):
    """
    This function is used to scrap the p tag from the html file.
    :param html_text: HTML text.
    :return: String of content in p tags. If error then False.
    """
    try:
        # Read the html text in Beautiful soup.
        soup = bs4.BeautifulSoup(str(html_text), "html.parser")

        # Get the html which having id as mw-content-text and class name as mw-parser-output.
        body_content = soup.find(id="mw-content-text").find(class_="mw-parser-output")

        # Convert the body_content string to Beautiful soup object.
        body_content_soup = bs4.BeautifulSoup(str(body_content), "html.parser")

        # Get the list of all the p tag in body_content and convert to string with adding whitespace in between.
        clean_body_content = " ".join(str(p.text) for p in body_content_soup.find_all('p'))
        return clean_body_content

    except Exception as e:
        # log the error.
        traceback.print_exc()
        logging.error("Failed to get the body content. Error: %s", e)
        return False


def run_scrapping():
    """" Start the scrapping of wikipedia articles and stores in the text files.
    """
    logging.info("Starting the scrapping process...")
    try:
        # Create an empty list variable.
        search_history = []
        # Run the for to scrap 2000 articles from wikipedia.
        for i in range(2000):

            # Send the request to wikipedia with the random url and get the response.
            response = requests.get(base_url)

            # Check if the current url is already exist in search_history list or not.
            if str(response.url) not in search_history:
                # if not exist then add it to the list.
                search_history.append(response.url)

                # Create the file with write mode and encoding format utf-8.
                f = open(module_directory + "/DataSet/" + str(i) + ".txt", "w", encoding="utf-8")
                # And write the response of get_body_content function.
                f.write(get_body_content(response.text))

            # Sleep for 2 second for not messing up with wikipedia server.
            sleep(2)

        # Save the search_history list which contains all the called urls into the file.
        f_ = open(module_directory + "/DataSet/url_list.txt", "w")
        f_.write("\n".join(search_history))

        return True

    except Exception as e:
        # log the error.
        traceback.print_exc()
        logging.error("Error: %s", e)
        print("Error: %s", e)
        return False


# Call the main method.
run_scrapping()
