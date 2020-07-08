'''
Hook for value extraction from question'

requirements - db_id, tokenized question, db_value_finder, potential_values,
               col_val_map for the db

desired ouput - list of values extracted from question of text type
'''

from named_entity_recognition.database_value_finder.database_value_finder import DatabaseValueFinder

DB_FOLDER = 'data/spider/original/database'
DB_SCHEMA = 'data/spider/original/tables.json'

all_database_value_finder = {}

def value_from_question(db_id, tokenized_question, candidates):
    db_value_finder = _get_or_create_value_finder(db_id)
    values = []
    stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
    potential_values = set([])
    tolerance = 0.75
    for token in tokenized_question:
        if token.lower() not in stopwords and token.lower() not in candidates:
            potential_values.add((token,tolerance))
    values = _find_matches_in_database(db_value_finder, potential_values)
    return list(set(values))

def _find_matches_in_database(db_value_finder, potential_values):
    matches = []
    print(
        f'Find potential candiates "{potential_values}" in database {db_value_finder.database}')
    try:
        matching_db_values = db_value_finder.find_similar_values_in_database(
            potential_values)
        matches = list(map(lambda v: v[0], matching_db_values))
    except Exception as e:
        print(
            f"!!!!!!!!!!!!!!!!!!!!!!! Error executing a query by the database finder. Error: {e}")
    return matches

def _get_or_create_value_finder(database):
    if database not in all_database_value_finder:
        all_database_value_finder[database] = DatabaseValueFinder(
            DB_FOLDER, database, DB_SCHEMA)
    db_value_finder = all_database_value_finder[database]
    return db_value_finder
