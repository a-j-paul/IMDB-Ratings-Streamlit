""" Streamlit app to display IMDB episode ratings """
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from get_data import get_show_data

# show app title
st.title("IMDB Ratings by Season and Episode")

# add instructions to sidebar
st.sidebar.markdown(
    """## Usage
1. Input URL of IMDB page for a TV show
2. Wait for ratings to be scraped, previously requested show ratings are cached
3. Use the multi-select to show/hide seasons"""
)

# show text input for IMDB URL
show_url = st.sidebar.text_input("IMDB URL", "https://www.imdb.com/title/tt0944947")

# get epsiode ratings, show name, etc.
df = get_show_data(show_url)
df["Season"] = df["Season"].astype(int)
show_name = df.name
seasons_list = sorted(set(df["Season"].to_list()), key=int)
episodes_list = sorted(set(df["Episode"].to_list()), key=int)

# show the show name
st.markdown(f"## {show_name}")

# multi-select to show/hide seasons
displayed_seasons = st.sidebar.multiselect(
    "Seasons to display", seasons_list, seasons_list,
)
hidden_seasons = sorted(set(seasons_list) - set(displayed_seasons), key=int)

# show heatmap
st.markdown("### Heatmap of Ratings vs. Season/Episode")
heatmap_df = df.pivot(index="Season", columns="Episode", values="Rating")[
    episodes_list
].drop(hidden_seasons)
f, ax = plt.subplots(figsize=(9, 6))
fig_heatmap = sns.heatmap(heatmap_df, annot=True, linewidths=0.5, ax=ax)
st.pyplot(fig_heatmap.figure)

# show line plot
st.markdown("### Lineplot of Ratings vs. Season/Episode")
line_df = df[~df["Season"].isin(hidden_seasons)]
sns.set(style="whitegrid")
f, ax = plt.subplots(figsize=(9, 6))
fig_line = sns.lineplot(
    x="Episode",
    y="Rating",
    hue="Season",
    data=line_df,
    legend="full",
    palette="deep",
    ax=ax,
)
st.pyplot(fig_line.figure)

# show data table
st.markdown("### Table of Data")
table_df = (
    df.pivot(index="Season", columns="Episode", values="Rating")[episodes_list]
    .drop(hidden_seasons)
    .style.format("{:.1f}")
)
st.dataframe(table_df)
