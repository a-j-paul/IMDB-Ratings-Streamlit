""" Get ratings data from IMDB """
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests
import seaborn as sns
from bs4 import BeautifulSoup

GOT_URL = "https://www.imdb.com/title/tt0944947"
AVATAR_URL = "https://www.imdb.com/title/tt0417299"
GREYS_URL = "https://www.imdb.com/title/tt0413573"


def get_episode_ratings_for_season(show_url: str, season: str = "1"):
    """ Get all episode ratings from a given season """
    data = []
    show_url = f"{show_url}/episodes?season={season}"
    response = requests.get(show_url)
    soup = BeautifulSoup(response.text, "html.parser")

    ratings_divs = soup.find_all("div", class_="ipl-rating-star small")

    epi = 1
    for rating_div in ratings_divs:
        rating = rating_div.find(class_="ipl-rating-star__rating").text
        data.append({"Season": season, "Episode": epi, "Rating": float(rating)})
        epi += 1

    return pd.DataFrame(data)


def get_seasons(show_url: str):
    """ Get all seasons """
    seasons = []
    show_url = f"{show_url}/episodes?season=1"
    response = requests.get(show_url)
    soup = BeautifulSoup(response.text, "html.parser")
    season_select_div = soup.find("div", class_="seasonAndYearNav").find("select")
    for option in season_select_div.find_all("option"):
        seasons.append(option.text.replace("\n", "").strip())
    return seasons


def get_show_name(show_url: str):
    """ Get show name """
    show_url = f"{show_url}/episodes?season=1"
    response = requests.get(show_url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.find("h3").find("a").text.replace("\n", "").strip()


def sanitize_url(show_url: str) -> str:
    """ Sanitize URL submitted by user """
    # TODO
    return ""


def get_show_data(show_url: str, reload_data: bool = False):
    """ Get all episode ratings for a given show """
    # get show name
    name = get_show_name(show_url)
    keepcharacters = (" ", ".", "_")
    safe_name = "".join(c for c in name if c.isalnum() or c in keepcharacters).rstrip()

    # read cached data from pickle file if available
    if Path(f"data\\{safe_name}.pkl").exists() and not reload_data:
        show_df = pd.read_pickle(f"data\\{safe_name}.pkl")
        show_df.name = safe_name
        return show_df

    # otherwise fetch new data and cache
    show_df = pd.DataFrame()
    for i in get_seasons(show_url):
        info = get_episode_ratings_for_season(show_url, season=i)
        show_df = show_df.append(info, ignore_index=True)
    show_df.name = safe_name
    show_df.to_pickle(f"data\\{safe_name}.pkl")

    return show_df


if __name__ == "__main__":
    show_data = get_show_data(GOT_URL, False).pivot(
        index="Season", columns="Episode", values="Rating"
    )
    print(show_data)

    f, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(show_data, annot=True, linewidths=0.5, ax=ax)
    plt.show()
