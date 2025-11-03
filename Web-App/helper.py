import numpy as np

def fetch_medal_tally(df,years, countries):
    medal_df = df.drop_duplicates(subset = ['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag = 0
    temp_df = medal_df

    if years == 'Overall' and countries == 'Overall':
        temp_df = medal_df
    if years == 'Overall' and countries != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == countries]
    if years != 'Overall' and countries == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(years)]
    if years != 'Overall' and countries != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(years)) & (medal_df['region'] == countries)]

    if flag == 1:
         x = (temp_df.groupby('Year').sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']].sort_values('Gold').reset_index())
    else:
        x = (
        temp_df.groupby('region')
        .sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']]
        .sort_values('Gold', ascending=False)
        .reset_index()
    )
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x



def medal_tally(df):

    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games',
                    'Year', 'City', 'Sport', 'Event', 'Medal'])

    medal_tally = medal_tally.groupby('region').sum()[['Gold',
           'Silver', 'Bronze']].sort_values('Gold',
            ascending=False).reset_index()

    medal_tally['total'] = (medal_tally['Gold'] +
            medal_tally['Silver'] + medal_tally['Bronze'])

    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['total'] = medal_tally['total'].astype('int')


    return medal_tally

def country_year(df):

    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    countries = np.unique(df['region'].dropna().values).tolist()
    countries.sort()
    countries.insert(0, 'Overall')

    return years, countries

def data_over_time(df,col):
    nations_over_time = (df.drop_duplicates(['Year', col])
    .groupby('Year').size().reset_index(name=col))
    nations_over_time.rename(columns={'Year': 'Edition',
                'count': col}, inplace=True)

    return nations_over_time

def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Compute medal counts
    x = (
        temp_df['Name']
        .value_counts()
        .reset_index()
        .head(15)
    )

    # Fix column names (unified for all pandas versions)
    x.columns = ['Name', 'Medals']

    # Merge to get sport & region
    x = x.merge(temp_df[['Name', 'Sport', 'region']], on='Name', how='left')
    x = x[['Name', 'Medals', 'Sport', 'region']].drop_duplicates(subset=['Name'])

    return x

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games',
    'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games',
    'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index = 'Sport',columns = 'Year',values = 'Medal',aggfunc = 'count' ).fillna(0)

    return pt

def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    # Compute medal counts
    x = (
        temp_df['Name']
        .value_counts()
        .reset_index()
        .head(10)
    )

    # Fix column names (unified for all pandas versions)
    x.columns = ['Name', 'Medals']

    # Merge to get sport & region
    x = x.merge(temp_df[['Name', 'Sport']], on='Name', how='left')
    x = x[['Name', 'Medals', 'Sport']].drop_duplicates(subset=['Name'])

    return x

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace = True)

    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final