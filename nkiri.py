#! /usr/bin/python3
# nkiri.py - Downloads movies from nkiri.com

import requests, sys, bs4, time, os


def parse_arguments(arg):
    try:
        arg_break = arg.index("-")
    except ValueError:
        return "+".join(arg[1:]), None
    search_word = "+".join(arg[1:arg_break])
    episode_nums = list(map(int, arg[arg_break + 1 :]))
    return search_word, episode_nums


def download_movie(url):
    filename = url.split("/")[-1]  # gets movie name from url

    if os.path.exists(filename):
        print(">>>{} exist \n".format(filename))
        return None

    print("Getting ready to download from {} (ctrl + z to quit)".format(url))
    r = requests.get(url, stream=True)
    r.raise_for_status()
    print(">>>Connected to {}".format(url))

    with open(filename, "wb") as f:
        print(">>>Downloading {}....".format(filename))
        for chunk in r.iter_content(100000):
            f.write(chunk)

    print(">>>Download complete {} \n".format(filename))


def user_choice(url_dict):
    """Displays url keys and returns url of the user's choice in dictionary"""

    print("Found {} result(s) ".format(len(url_dict)).center(80, "-"))

    # exit if no search result
    if len(url_dict) == 0:
        print("\nExiting...")
        time.sleep(3)
        sys.exit()

    url_keys = list(url_dict.keys())
    for num, key in enumerate(url_keys):
        print("{}. {}".format(num + 1, key))

    # validate user input
    while True:
        try:
            user_input = int(
                input("Please select a number from above (or ctrl + z to quit)\n")
            )
        except ValueError:
            continue
        else:
            if user_input not in range(1, len(url_keys) + 1):
                continue
            else:
                break
    print("Retrieving page #{}: {}... \n".format(user_input, url_keys[user_input - 1]))
    return url_dict[url_keys[user_input - 1]]


def main():
    search_word, episode_nums = parse_arguments(sys.argv)

    # get search page in nkiri
    search_page = requests.get(
        "https://nkiri.com/?s=" + search_word + "&post_type=post"
    )
    search_page.raise_for_status()

    # find movies link from search result
    search_parser = bs4.BeautifulSoup(search_page.text, "html.parser")
    search_elems = search_parser.findAll("a", {"rel": "bookmark"})

    search_dict = {
        search_elem.get("title"): search_elem.get("href")
        for search_elem in search_elems
    }

    user_input = user_choice(search_dict)

    # get page of movie selected
    movie_page = requests.get(user_input)
    movie_page.raise_for_status()

    # find all movies download link in page
    movie_parser = bs4.BeautifulSoup(movie_page.text, "html.parser")
    movie_elems = movie_parser.findAll(
        "a", {"class": "elementor-button-link elementor-button elementor-size-md"}
    )

    if len(movie_elems) == 0:
        print("No movie found")

    for movie_elem in movie_elems:
        download_link = movie_elem.get("href")
        episode_num = movie_elems.index(movie_elem) + 1

        if (movie_elem.get_text().strip() == "Download Episode") and (
            episode_nums == None or episode_num in episode_nums
        ):
            download_movie(download_link)

        elif movie_elem.get_text().strip() == "Download Movie":
            download_movie(download_link)


if __name__ == "__main__":
    main()
