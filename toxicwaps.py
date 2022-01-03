#! python3
# toxicwaps.py - Download movies from toxicwaps.com

import requests, sys, bs4, time, os
from nkiri import parse_arguments, download_movie, choice


def parser(url):
    "Returns the bs4 object for the page url"
    headers = {"user-agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    r.raise_for_status()

    parser = bs4.BeautifulSoup(r.text, "lxml")
    return parser


def main():

    # TODO: get and parse search result
    search_word, episode_num = parse_arguments(sys.argv)
    search_url = "https://dokisuru.com/?q=" + search_word
    search_parser = parser(search_url)
    search_elements = search_parser.find_all(
        "a", {"class": "ui-btn ui-btn-icon-right ui-icon-carat-r"}
    )
    print(search_elements)
    movie_list = {
        search_element.getText(): search_element.get("href")
        for search_element in search_elements
    }
    print(movie_list)


# TODO: get and parse movie page seasons url

# TODO: get and parse season page for episodes url

# TODO: get and parse download page for download url


if __name__ == "__main__":
    main()
