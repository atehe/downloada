#! python3
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
    filename = url.split("/")[-1]
    if os.path.exists(filename):
        print("**{} exist**".format(filename))
        return None
    r = requests.get(url, stream=True)
    r.raise_for_status()
    print("Connected to {}".format(url))

    with open(filename, "wb") as f:
        print("Downloading {}....".format(filename))
        for chunk in r.iter_content(100000):
            f.write(chunk)

    print("\n>>>Download complete {} \n".format(filename))


def main():
    search_word, episode_nums = parse_arguments(sys.argv)

    # get search page in nkiri
    search_page = requests.get(
        "https://nkiri.com/?s=" + search_word + "&post_type=post"
    )
    search_page.raise_for_status()

    # find movies link from search result
    search_parser = bs4.BeautifulSoup(search_page.text, "html.parser")
    search_elems = search_parser.findAll("a", {"title": "Continue Reading"})

    movie_links = [movies_elem.get("href") for movies_elem in search_elems]

    print(" Found {} result(s) ".format(len(movie_links)).center(80, "-"))

    # exit if no search result
    if len(movie_links) == 0:
        print("\nExiting...")
        time.sleep(3)
        sys.exit()

    for search_num, movie_link in enumerate(movie_links):
        print("{}. {}".format(search_num + 1, movie_link))

    # validate user input
    while True:
        try:
            user_input = int(
                input("Please select a number from above (or ctrl + z to quit)\n")
            )
        except ValueError:
            continue
        else:
            if user_input not in range(1, len(movie_links) + 1):
                continue
            else:
                break

    print(
        "Retrieving page #{}: {}... \n".format(user_input, movie_links[user_input - 1])
    )

    # get page of movie selected
    movie_page = requests.get(movie_links[user_input - 1])
    movie_page.raise_for_status()

    # find all movies download link in page
    movies_parser = bs4.BeautifulSoup(movie_page.text, "html.parser")
    movies_elem = movies_parser.findAll(
        "a", {"class": "elementor-button-link elementor-button elementor-size-md"}
    )

    if movies_elem == []:
        print("No movie found")

    episode_num = 0
    for movie_elem in movies_elem:
        download_link = movie_elem.get("href")
        if movie_elem.get_text().strip() == "Download Episode":
            episode_num += 1
            if episode_num in episode_nums or episode_nums == None:
                download_movie(download_link)

        elif movie_elem.get_text().strip() == "Download Movie":
            download_movie(download_link)


if __name__ == "__main__":
    main()
