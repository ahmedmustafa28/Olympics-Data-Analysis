import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

@st.cache_data
def load_data():
    df = pd.read_csv('athlete_events.csv')
    region_df = pd.read_csv('noc_regions.csv')
    df = preprocessor.preprocess(df, region_df)
    return df

df = load_data()

st.sidebar.title("Olympics Analysis")
st.sidebar.image('image.png')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal-Tally','Overall Analysis','Country-Wise Analysis',
     'Athlete-Wise Analysis')
)

@st.cache_data
def get_medal_tally(df, year, country):
    return helper.fetch_medal_tally(df, year, country)

@st.cache_data
def get_data_over_time(df, col):
    return helper.data_over_time(df, col)

@st.cache_data
def get_yearwise_medal_tally(df, country):
    return helper.yearwise_medal_tally(df, country)

@st.cache_data
def get_country_event_heatmap(df, country):
    return helper.country_event_heatmap(df, country)

@st.cache_data
def get_most_successful(df, sport):
    return helper.most_successful(df, sport)

@st.cache_data
def get_most_successful_countrywise(df, country):
    return helper.most_successful_countrywise(df, country)


if user_menu == 'Medal-Tally':
    st.sidebar.header("Medal Tally")
    years, countries = helper.country_year(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_countries = st.sidebar.selectbox("Select Country", countries)

    medal_tally = get_medal_tally(df, selected_year, selected_countries)

    if selected_year == 'Overall' and selected_countries == 'Overall':
        st.title("Overall tally")
    if selected_year != 'Overall' and selected_countries == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_countries != 'Overall':
        st.title(selected_countries + " Overall Performance")
    if selected_year != 'Overall' and selected_countries != 'Overall':
        st.title(selected_countries + " performance in " + str(selected_year) + " Olympics")

    st.table(medal_tally)


if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    st.title("Participating Nations Over the Years")
    nations_over_time = get_data_over_time(df, 'region')
    fig = px.line(nations_over_time, x='Edition', y='region')
    st.plotly_chart(fig)

    st.title("Events Over the Years")
    events_over_time = get_data_over_time(df, 'Event')
    fig = px.line(events_over_time, x='Edition', y='Event')
    st.plotly_chart(fig)

    st.title("Athletes Over the Years")
    athletes_over_time = get_data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x='Edition', y='Name')
    st.plotly_chart(fig)

    st.title("No. of Events Over Time (Every Sport)")
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    fig, ax = plt.subplots(figsize=(12, 8))
    ax = sns.heatmap(
        x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
        annot=True
    )
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    most_successful_df = get_most_successful(df, selected_sport)
    st.table(most_successful_df)


if user_menu == 'Country-Wise Analysis':
    st.sidebar.title("Country-Wise Analysis")

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    country_df = get_yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country + " Medal Tally Over the Years")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")
    pt = get_country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(12, 8))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title("Top 10 Athletes of " + selected_country)
    top10_df = get_most_successful_countrywise(df, selected_country)
    st.table(top10_df)

if user_menu == 'Athlete-Wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age',
    'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
    show_hist=False, show_rug=False)
    fig.update_layout(autosize = False, width = 1000, height = 600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing', 'Equestrianism',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Modern Pentathlon', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens', 'Trampolining',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Lacrosse', 'Polo',
                     'Cricket', 'Ice Hockey', 'Racquets', 'Motorboating', 'Croquet',
                     'Figure Skating', 'Jeu De Paume', 'Roque', 'Basque Pelota',
                     'Alpinism', 'Aeronautics']

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        data = temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna()

        # ✅ Fix: Must have at least 2 values and not all identical
        if len(data) > 1 and data.std() > 0:
            x.append(data)
            name.append(sport)

    if len(x) > 0:
        fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
        fig.update_layout(autosize=False, width=1000, height=600)
        st.title("Distribution of Age w.r.t Sports (Gold Medalist)")
        st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(x='Weight', y='Height', data=temp_df,
    hue = temp_df['Medal'],style = temp_df['Sex'], s = 60)

    st.pyplot(fig)

    st.title('Men vs Women Participation over the Years')
    final = helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

