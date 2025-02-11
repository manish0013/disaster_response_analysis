
import pandas as pd
from sqlalchemy import create_engine
import sys

def load_data(messages_filepath, categories_filepath):
    # load messages dataset
    messages = pd.read_csv(str(messages_filepath))
    categories = pd.read_csv(str(categories_filepath))
    # merge datasets
    df = messages.merge(categories,on='id')
    # create a dataframe of the 36 individual category columns
    categories = categories.categories.str.split(pat=';',expand=True)

    # select the first row of the categories dataframe
    row = categories.loc[0]
    category_colnames = row.apply(lambda x: x[:-2]).values
    # rename the columns of `categories`
    categories.columns = category_colnames
    for column in categories:
        # set each value to be the last character of the string
        categories[column] = categories[column].astype(str).apply(lambda x: x[-1])

        # convert column from string to numeric
        categories[column] = categories[column].astype(int)
        
    # concatenate the original dataframe with the new `categories` dataframe
    df = pd.concat([df,categories],axis = 1)
    return df
    

def clean_data(df):
    # drop duplicates
    df = df[~df.duplicated()]
    return df

def save_data(df, database_filename):
    engine = create_engine('sqlite:///' + str(database_filename))
    df.to_sql('twt_disaster_clean', engine, if_exists='replace',index=False)


def main():
    # import libraries

    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        print(df.head())
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()