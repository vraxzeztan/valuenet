'''
Hook for value extraction from question'

requirements - db_id, tokenized question, db_value_finder, potential_values,
               col_val_map for the db

desired ouput - list of values extracted from question of text type
'''
import json
from named_entity_recognition.database_value_finder.database_value_finder import DatabaseValueFinder

db_id = None
stopwords = None
col_val_map = None
potential_values = None
tokenized_question = None
db_value_finder = DatabaseValueFinder()

values = []
for token in tokenized_question:
    if token not in stopwords and token not in potential_values:
        match = db_value_finder(token, None)
        val, col, table = match
        if(val in col_val_map[col]):
            values.append(val)

return values