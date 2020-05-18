""" Streamlit app to display IMDB episode ratings """
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

from get_data import get_show_data

# show app title
st.title("IMDB Ratings by Season and Episode")

# show text input for IMDB URL
show_url = st.text_input("IMDB URL", "https://www.imdb.com/title/tt0944947")

# get epsiode ratings, show name, etc.
df = get_show_data(show_url)
show_name = df.name
seasons_list = sorted(set(df["Season"].to_list()), key=int)
episodes_list = sorted(set(df["Episode"].to_list()), key=int)

# show the show name
st.markdown(f"## {show_name}")

# multi-select to show/hide seasons
displayed_seasons = st.multiselect("Seasons to display", seasons_list, seasons_list,)
hidden_seasons = sorted(set(seasons_list) - set(displayed_seasons), key=int)

# show data table
st.dataframe(
    df.pivot(index="Season", columns="Episode", values="Rating")[episodes_list]
    .drop(hidden_seasons)
    .style.format("{:.1f}")
)

# show line plot
plot_df = df[~df["Season"].isin(hidden_seasons)]
sns.set(style="whitegrid")
fig = sns.lineplot(
    x="Episode", y="Rating", hue="Season", data=plot_df, legend="full", palette="deep",
)
st.pyplot(fig.figure)
