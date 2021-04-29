#!/usr/bin/env python3

from nltk.stem import WordNetLemmatizer
from collections import OrderedDict
from src.Preprocessing import Porter
from collections import defaultdict
from nltk.stem.porter import *
import re
import sys
import math
import nltk


class BooleanRetrievalModel():

    def __init__(self):
        self.short_stories_path = './dist/ShortStories'
        self.id_token_dict_path = './dist/Total-Words.csv'
        self.positional_index_path = './dist/positional.txt'
        self.wordnet_lemmatizer = WordNetLemmatizer()
        self.stemmer = PorterStemmer()

    def GetTokenDictionary(self, filename: str):

        __token_to_id_dict = {}

        try:
            with open(filename, mode='r') as file:
                for line in file:
                    __tokens = line.split(',')
                    __token_to_id_dict[__tokens[1]] = __tokens[0]
        except FileNotFoundError:
            print('File not found!')
            sys.exit(1)

        return __token_to_id_dict

    def TokensToId(self, tokens: list, tokens_to_id_dict: dict):
        __token_to_id = []
        for token in tokens:
            if token not in tokens_to_id_dict:
                tokens_to_id_dict[token] = str(len(tokens_to_id_dict))
            __token_to_id.append(str(tokens_to_id_dict[token]))

        return __token_to_id

    def PreprocessQuery(self, query: str):
        __tokens = query.split(' ')

        # Very annoying UTF 8 characters
        very_annoying_utf_8_characters = [
            '\n', '\r', '\"', '\'', '.', '’', ',', '“' '”', ';', '“', '!', '”', '”', '“', '-']

        for idx, _ in enumerate(__tokens):
            for remove_character in very_annoying_utf_8_characters:
                __tokens[idx] = __tokens[idx].replace(remove_character, ' ')
                __tokens[idx] = re.sub(' +', ' ', __tokens[idx].strip())

        __tokens = ' '.join([entry for entry in __tokens if entry !=
                             '' and not entry.isnumeric()])

        __tokens = [token.lower() for token in __tokens.split(' ')]

        # Custom method
        # STEMMING ->> LEMMATIZATION
        # __tokens = [self.wordnet_lemmatizer.lemmatize(
        # Porter.CustomPorterAlgorithm(token)) for token in __tokens]

        # Using Porter's algorithm
        # STEMMING ->> LEMMATIZATION
        __tokens = [self.wordnet_lemmatizer.lemmatize(
            self.stemmer.stem(token)) for token in __tokens]

        return __tokens

    def GetPositionalIndex(self, tokens_to_id: list):
        __id_with_positions = {}
        with open(self.positional_index_path, mode='r') as file:
            for line in file:
                line_split_token = line.split('-')
                if line_split_token[0] in tokens_to_id:
                    __id_with_positions[line_split_token[0]
                                        ] = line_split_token[1]

        return __id_with_positions

    def ExtractOnlyDocuments(self, id_with_positions: dict):
        __document_ids = defaultdict(list)
        for key, value in id_with_positions.items():
            split_docs = value.split(';')
            for docs in split_docs:
                doc_id = docs.split(',')[0]
                if doc_id not in __document_ids and doc_id != '\n':
                    __document_ids[key].append(docs.split(',')[0])
        return __document_ids

    def IntersectDocuments(self, documents_per_word: dict):

        doc_key_1 = next(iter(documents_per_word))
        doc_key_2 = next(iter(documents_per_word))

        doc_list_1 = documents_per_word[doc_key_1]
        doc_list_2 = documents_per_word[doc_key_2]

        __intersect_documents = [
            value for value in doc_list_1 if value in doc_list_2]

        for (_, value) in (documents_per_word.items()):
            __intersect_documents = [
                doc_id for doc_id in __intersect_documents if doc_id in value]

        return __intersect_documents

    def QueryDocPositions(self, query: str,
                          documents_per_word: list,
                          id_with_positions: dict) -> list:

        positions = []
        query_len = len(query)

        for _, value in id_with_positions.items():
            value_split_for_docs = value.split(';')
            for doc_space in value_split_for_docs:
                if doc_space.split(',')[0] in documents_per_word:
                    for entry in doc_space.split(',')[1]:
                        positions.append(int(entry))

        positions.sort()

        continue_count = 0
        for index in range(0, len(positions)):
            if positions[index] + 1 == positions[index + 1]:
                continue_count += 1
            else:
                continue_count = 0

            if continue_count == query_len:
                return positions

        return []

    def SimpleBooleanQuery(self, query: str):


        # Preprocess and convert the tokens to their respective IDs
        __tokens_to_id = self.TokensToId(
            self.PreprocessQuery(query), self.GetTokenDictionary(self.id_token_dict_path))

        __positional_indexes = self.GetPositionalIndex(__tokens_to_id)

        __document_ids = self.ExtractOnlyDocuments(__positional_indexes)

        if len(__document_ids) == 0:
            return []
        elif len(__document_ids) == 1:
            for _, value in __document_ids.items():
                return value
        else:
            __intersected_docs = self.IntersectDocuments(__document_ids)

            return self.QueryDocPositions(
                query, __intersected_docs, __positional_indexes)

    def ORQuery(self, document_1, document_2):
        return list(dict.fromkeys(document_1 + document_2))

    def ANDQuery(self, document_1, document_2):
        return [entry for entry in document_1 if entry in document_2]

    def InvertDocumentNOTQuery(self, document_list: list):
        return [doc_id for doc_id in range(1, 50 + 1) if doc_id not in document_list]

    def NOTQuery(self, document_1, document_2):
        return [document for document in document_1 if document not in document_2]

    def BoolOperationHandler(self, document_list_1: list, document_list_2: str, operator: str):
        if operator == 'and':
            return self.ANDQuery(document_list_1, document_list_2)
        elif operator == 'or':
            return self.ORQuery(document_list_1, document_list_2)
        elif operator == 'not':
            return self.NOTQuery(document_list_1, document_list_2)

    def ComplexBooleanQuery(self, query: str):

        phrases, operators, init_pos, final_phrases, final_doc_results, query_results, __tokens = [
        ], [], 0, [], [], [], [token.lower() for token in query.strip(' ').split(' ')]

        # Check for correct syntax
        for i in range(0, len(__tokens) - 1):
            if (__tokens[i] == 'or' and __tokens[i + 1] == 'or') or \
                (__tokens[i] == 'and' and __tokens[i + 1] == 'and') or \
                    __tokens[i] == 'not' and __tokens[i + 1] == 'not':
                return "Invalid query structure!"

        for index, token in enumerate(__tokens):
            if token == 'and' or token == 'or' or token == 'not':
                phrases.append(__tokens[init_pos:index])
                init_pos = index + 1
                if token == 'and':
                    operators.append('and')
                elif token == 'or':
                    operators.append('or')
                elif token == 'not':
                    operators.append('not')

            if index + 1 == len(__tokens):
                phrases.append(str(__tokens[-1]))

        for phrase in phrases:
            if phrase != []:
                if type(phrase) is list and len(phrase) == 1:
                    final_phrases.append(phrase[0])
                else:
                    final_phrases.append(phrase)

        # Preprocessing the operators list
        operators = [operator for operator in operators if operator != []]

        # No operators involved! Easy
        if len(final_phrases) == 1:
            return self.SimpleBooleanQuery(final_phrases[0])

        # print(final_phrases, operators)
        # return [1, 2, 3]

        for idx, phrase in enumerate(final_phrases):

            try:
                if operators[idx] == 'not':
                    final_doc_results.append(self.InvertDocumentNOTQuery(
                        self.SimpleBooleanQuery(phrase)))
                    operators.pop(idx)
                else:
                    final_doc_results.append(self.SimpleBooleanQuery(phrase))
            except IndexError:
                # Index not found - let it go
                pass

        query_results.append(final_doc_results[0])

        for i in range(0, len(operators)):
            query_results.append(self.BoolOperationHandler(
                query_results[i], final_doc_results[i], operators[i]))

        return query_results[len(query_results) - 1]

    def ProximityQuery(self, query: str):

        tokens = query.split(' ')

        max_window_size = 0
        words, preprocessed = [], []
        for token in tokens:
            if token.startswith('/'):
                if int(token[1:len(token)]) > max_window_size:
                    max_window_size = int(token[1:len(token)])
            else:
                words.append(token)

        for word in words:
            preprocessed.append(self.PreprocessQuery(word))

        documents = []
        for i in range(0, 50):
            file_data = ''
            with open(f"{self.short_stories_path}/{i + 1}.txt", mode='r') as file:
                file_data = file.readlines()

            file_data = file_data[0].split(' ')

            init_pos, fin_pos = math.ceil(max_window_size / 2), len(file_data)
            for index in range(init_pos, fin_pos):
                for word in words:
                    if word in file_data[index - init_pos: index + init_pos] and i not in documents:
                        documents.append(i)

        return documents

    def ResolveQuery(self, query: str, option: int):

        if option == 0:
            return self.SimpleBooleanQuery(query)
        elif option == 1:
            return self.ComplexBooleanQuery(query)
        elif option == 2:
            return self.ProximityQuery(query)
