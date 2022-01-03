#! python3
# netnaija.py - Downloads movie from netnaija

import requests, sys, bs4, time, os, lxml
from nkiri import download_movie, choice, parse_arguments


def get_seasons_link(movie_link):
    # get and parse movie page for seasons link
    movie_page = requests.get(movie_link)
    movie_page.raise_for_status()

    season_parser = bs4.BeautifulSoup(movie_page.text, "html.parser")
    season_elems = season_parser.findAll("div", {"class": "video-seasons"})

    season_urls = [season_elem.find("a").get("href") for season_elem in season_elems]
    return season_urls


def get_episodes_link(season_url):
    episodes_page = requests.get(season_url)
    episodes_page.raise_for_status()

    episodes_parser = bs4.BeautifulSoup(episodes_page.text, "html.parser")
    episode_elems = episodes_parser.findAll("a", {"class": "anchor"})

    episodes_url = [episode_elem.get("href") for episode_elem in episode_elems]
    return episodes_url


def get_sabishare(episode_link):
    sabishare_page = requests.get(episode_link)
    sabishare_page.raise_for_status()

    sabishare_parser = bs4.BeautifulSoup(sabishare_page.text, "html.parser")
    download_page_link = sabishare_parser.find("a", {"title": "Download Video"})
    susbtitle_page_link = sabishare_parser.find("a", {"title": "Download Subtitle"})
    print(download_page_link, susbtitle_page_link)
    return download_page_link, susbtitle_page_link


def main():
    # get search page iin netnaija
    search_word, episode_num = parse_arguments(sys.argv)
    search_page = requests.get(
        "https://www.thenetnaija.co/search?folder=&t=" + search_word
    )
    search_page.raise_for_status()

    search_parser = bs4.BeautifulSoup(search_page.text, "html.parser")
    search_elems = search_parser.findAll("div", {"class": "info"})

    # get movies link from search result
    movie_links = [
        search_elem.find("a").get("href")
        for search_elem in search_elems
        if "Series" in search_elem.find("a").get_text()
    ]

    # prints movies link and prompt for user input
    movie_input = choice(movie_links)

    seasons = get_seasons_link(movie_input)
    season_url = choice(seasons)

    episodes_link = get_episodes_link(season_url)

    get_sabishare(
        episodes_link[0]
    )  ## href returns a local file path (no futher crawling possible), best try selenuim


if __name__ == "__main__":
    main()
