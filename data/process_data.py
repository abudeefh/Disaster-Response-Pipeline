import sys
import pandas as pd

from sqlalchemy import create_engine

def convert_categories_to_numerical(categories: pd.DataFrame)->pd.DataFrame:
    '''
    Function for changing categorical data to numeric (0 and 1).
    Arguments: the DataFrame/ categories
    Returns: numerical/ dataencoded categories
    '''
    for col in categories:

        categories[col] = categories[col].map(
            lambda x: 1 if int(x.split("-")[1]) > 0 else 0 )
    return categories

def split_categories(categories: pd.DataFrame)->pd.DataFrame:
    '''
    Function for transforming categories to one-hot encoded format
    Arguments: the DataFrame/ categories
    Returns: numerical/ dataencoded categories
    '''
    categories = categories['categories'].str.split(';',expand=True)
    row = categories.iloc[[1]].values[0]
    categories.columns = [ x.split("-")[0] for x in row]
    categories = convert_categories_to_numerical(categories)
    return categories

def load_data(messages_filepath: str, categories_filepath: str)->pd.DataFrame:
    '''
    Function for loading the 2 datasets into 1 master dataset
    Arguments:   messages_filepath: The file path to the messages.csv file
            categories_filepath: The file path to the categories.csv file
    Returns: A pandas DataFrame containing both files
    '''
    messages = pd.read_csv(messages_filepath)
    categories = split_categories(pd.read_csv(categories_filepath))

    return pd.concat([messages,categories],join="inner", axis=1)

def clean_data(df: pd.DataFrame)->pd.DataFrame:
    '''
    Function for cleaning data, dropping duplicates
    Arguments: pandas DataFrame gross with duplicate
    Returns: pandas DataFrame net with no duplicates
    '''
    return df.drop_duplicates()

def save_data(df: pd.DataFrame, database_filename: str)->None:
    '''
    Function for saving the database in an sql file
    Arguments:   df: The pandas DataFrame which shall be saved
            database_filename: The path where the sql database shall be saved
    Returns: N/A
    '''
    engine = create_engine('sqlite:///{}'.format(database_filename))
    df.to_sql('disaster_response', engine, if_exists='replace', index=False)

def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)

        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)

        print('Cleaned data saved to database!')

    else:
        print('Please provide filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()