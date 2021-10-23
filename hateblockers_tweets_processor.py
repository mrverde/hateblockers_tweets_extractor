import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def processor():
    columns = ["search_term", "user", "user_name", "twit_id", "created_at", "favorite_count",
               "retweet_count", "text", "hashtags", "user_mentions",
               "urls", "in_reply_to_status_id", "in_reply_to_status_id_str",
               "in_reply_to_user_id", "in_reply_to_screen_name", "text_range", "geo", "coordinates"]

    df = pd.read_csv("exports/2021-10-23 - SEARCH.csv",
                     sep="\t")

    df.columns = columns

    df = df[["search_term", "created_at", "favorite_count", "retweet_count"]]

    # Twits por término
    print(df["search_term"].value_counts())

    # Término por hora
    df_hour = df[["search_term", "created_at"]]
    df_hour.columns = ["search_term", "hour"]
    df_hour.iloc[:, 1] = df_hour.iloc[:, 1].str[11:13].astype(int)
    df_hour["n_twits"] = 1
    df_hour = pd.pivot_table(df_hour, index=['search_term'], columns=[
                             'hour'], aggfunc=np.sum)
    df_hour = df_hour.fillna(0)
    df_hour = df_hour.astype(int)
    print(df_hour)

    # Retweets / Favoritos por término
    print(df[["search_term", "favorite_count", "retweet_count"]]
          .groupby(["search_term"]).sum())


if __name__ == "__main__":
    processor()
