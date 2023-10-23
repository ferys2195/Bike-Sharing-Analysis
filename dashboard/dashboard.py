import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
import calendar

sns.set(style='dark')

# mengatur warna chart
chart_color = ["#90CAF9", "#D3D3D3"]
color_primary, color_secondary = chart_color


def create_compare_year_df(dataframe):
    data = dataframe.groupby(by="yr").agg({"cnt": "sum"}).reset_index()
    data["yr"] = data["yr"].astype(str)
    return data


def create_performance_df(dataframe):
    compare_per_year = (dataframe.groupby(by=["yr", "mnth"])
                        .agg({"cnt": "sum"})
                        .sort_values(by=["yr", "mnth"], ascending=True)
                        .reset_index())

    pivot_df = compare_per_year.pivot(index='mnth', columns='yr', values='cnt')

    month_names = [calendar.month_abbr[i] for i in pivot_df.index]

    pivot_df.index = month_names

    pivot_df.columns = [str(col) for col in pivot_df.columns]

    return pivot_df


def create_season_df(dataframe):
    return dataframe.groupby(by="season").agg({"cnt": "sum"}).sort_values(by="cnt", ascending=True).reset_index()


def create_day_df(dataframe):
    return dataframe.groupby(by=["weekday"]).agg({"cnt": "sum"}).sort_values(by=["cnt"], ascending=True).reset_index()


# initial data frame
df = pd.read_csv("./dashboard/main_data.csv")
performance_df = create_performance_df(df)
season_df = create_season_df(df)
day_df = create_day_df(df)
compare_year_df = create_compare_year_df(df)

st.header("Bike Sharing Dashboard")

st.subheader('Summary')
col1, col2 = st.columns(2, gap="large")

with col1:
    total_orders = df.agg({'cnt': 'sum'})
    st.metric("Total orders", value=int(total_orders))

with col2:
    total_revenue = df.agg({'cnt': 'mean'})
    st.metric("Average per day", value=int(total_revenue))

with st.container():
    fig, ax = plt.subplots(figsize=(16, 8))
    x = np.array(compare_year_df["yr"])
    y = np.array(compare_year_df["cnt"])

    ax.bar(x, y, color=chart_color[::-1])
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.set_title('Bike Sharing Comparison by Year', loc="center", fontsize=25)
    ax.tick_params(axis='y', labelsize=18)
    ax.tick_params(axis='x', labelsize=24)

    st.pyplot(fig)

with st.container():

    fig, ax = plt.subplots(figsize=(16, 8))
    index_list = performance_df.index.tolist()
    year_2011_list = performance_df["2011"].tolist()
    year_2012_list = performance_df["2012"].tolist()

    # Menghitung lebar bar
    bar_width = 0.35

    # Membuat posisi x untuk bar chart
    r1 = np.arange(len(index_list))
    r2 = [x + bar_width for x in r1]

    # Membuat grouped bar chart
    ax.bar(r1, year_2011_list, color=color_secondary, width=bar_width, edgecolor='grey', label='2011')
    ax.bar(r2, year_2012_list, color=color_primary, width=bar_width, edgecolor='grey', label='2012')

    # Menentukan label pada sumbu x dan y
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.tick_params(axis='y', labelsize=18)
    ax.tick_params(axis='x', labelsize=20)

    ax.set_title("Bike Sharing Comparison Every Month in Between Year", loc="center", fontsize=25)

    # Menentukan label pada sumbu x
    ax.set_xticks([r + bar_width / 2 for r in range(len(index_list))], index_list)

    # Menambahkan label pada bar chart
    ax.legend(fontsize=18)

    st.pyplot(fig)

st.subheader("Best Bike Sharing Based on Season and day")
with st.container():
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(25, 15))

    max_value = max(season_df['cnt'])
    colors = []
    for c in range(len(season_df["cnt"])):
        colors.append(color_primary if season_df['cnt'][c] == max_value else color_secondary)

    ax[0].barh(season_df["season"], season_df["cnt"], color=colors)
    ax[0].set_title("Number of Order Based on Season", fontsize=35)
    ax[0].tick_params(axis='y', labelsize=35)
    ax[0].tick_params(axis='x', labelsize=30)

    day_names = [calendar.day_name[i] for i in day_df["weekday"]]
    day_df["weekday"] = day_names
    max_value = max(day_df['cnt'])
    colors = []
    for c in range(len(day_df["cnt"])):
        colors.append(color_primary if day_df['cnt'][c] == max_value else color_secondary)

    ax[1].barh(day_df["weekday"], day_df["cnt"], color=colors)
    ax[1].set_title("Number of Order by Day", loc="center", fontsize=35)
    # ax[1].invert_xaxis()
    ax[1].yaxis.tick_right()
    ax[1].tick_params(axis='y', labelsize=35)
    ax[1].tick_params(axis='x', labelsize=30)

    st.pyplot(fig)

st.subheader("Users Demographics")
with st.container():
    fig, ax = plt.subplots(figsize=(5, 5))
    users = df.agg({"casual": "sum", "registered": "sum"}).reset_index()
    ax.pie(users[0], colors=chart_color[::-1], autopct='%1.1f%%', labels=users["index"], wedgeprops=dict(width=0.6))
    ax.set_title("Percentage of Bike Sharing Users", fontsize=10)
    st.pyplot(fig)
