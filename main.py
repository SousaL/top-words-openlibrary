"""
Author  Leonardo Pedro da Silva de Sousa
Date    26/08/2019
"""

import configparser
import argparse
import pymongo
import pandas as pd
from loguru import logger
from api_open_library import ApiOpenLibrary

def del_if_bd_exists(client, name):
    """
    Args:
        client: instance from mongodb
        name:  database's name
    """
    client.drop_database(name)


def get_db(name):
    """
    Args:
        name:  database's name
    Returns:
        The database instance
    """
    client = pymongo.MongoClient()

    del_if_bd_exists(client, name)

    database = client[name]

    return database


def insert_on_bd(database, data):
    """
    Args:
        database: database instance
        data: result downloaded from the openlibrary
    """
    books = database.books

    if not data:
        logger.info(f'No Results, try again...')
        return

    books.insert_many(data)
    database.profiles.create_index([('title', pymongo.ASCENDING)])

    del data


def pipeline_top_n_words(n_words=10):
    """ Create pipeline for use in collection aggregate
    Args:
        n_words: number of words to limit
    Returns:
        The pipeline with the operations to be performed
    """
    pipeline = [{"$project": {"title": {"$toUpper": "$title"}}},
                {"$project": {"words": {"$split": ["$title", " "]}}},
                {"$unwind": "$words"},
                {"$match": {"$expr": {"$gt": [{"$strLenCP": "$words"}, 5]}}},
                {"$group": {"_id": "$words", "count": {"$sum": 1}}},
                {"$sort": {"count": -1, "_id": 1}},
                {"$limit": n_words}
                ]
    return pipeline


def get_top_words(database, n_words):
    """ Get the top words in the `books` collection
    Args:
        client: instance from mongodb
        name:  database's name
    """

    pipeline = pipeline_top_n_words(n_words)

    result = [word for word in database.books.aggregate(pipeline)]

    return result


def main():
    """ Main function
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('query', nargs='+', default=[], help='query')
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read('config.ini')
    db_name = config['DB']['Database_name']
    n_words = int(config['DEFAULT']['N_words'])
    api_src = config['DEFAULT']['Api_src']

    search = ' '.join(args.query)

    api = ApiOpenLibrary(api_src)
    response = api.query(search)

    database = get_db(db_name)
    insert_on_bd(database, response)

    top_words = get_top_words(database, n_words)
    data_frame = pd.DataFrame(data=top_words)
    data_frame.index += 1
    data_frame = data_frame.rename(columns={'_id': 'Words', 'count': 'Total'})
    logger.info(f'\n{data_frame}')


if __name__ == '__main__':
    main()
