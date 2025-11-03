import pandas as pd

def preprocess(df,region_df):

    # Filter for Summer Olympics only
    df = df[df['Season'] == 'Summer']

    # Merge with region_df safely
    df = df.merge(region_df[['NOC', 'region', 'notes']], on='NOC', how='left')

    # Drop duplicates
    df.drop_duplicates(inplace=True)

    # One-hot encode medals only (not region)
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)

    return df
