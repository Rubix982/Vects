from Preprocessing import AuxPreprocessing
import pandas as pd
import numpy as np
import operator
import math
import os


class TermFrequencyIndexer():

    short_stories_path = os.path.abspath('.') + "/dist/ShortStories"

    def __init__(self, list_of_filenames: list = os.listdir(short_stories_path)):
        self.list_of_filenames = list_of_filenames

    def IndexShortStories(self):

        df = pd.DataFrame(
            columns=['word'] + [f'df{i}' for i in range(1, 50 + 1)])

        count_dict = {}
        for filename in self.list_of_filenames:
            with open(self.short_stories_path + "/" + filename, mode='r') as file:
                data = str(file.read()).split(' ')
                index = filename.split('.')[0]
                for token in data:
                    if token not in count_dict:
                        count_dict[token] = {}
                        count_dict[token][index] = 1
                    else:
                        if index not in count_dict[token]:
                            count_dict[token][index] = 0
                        count_dict[token][index] += 1

        for key, _ in count_dict.items():
            df = df.append(pd.DataFrame(
                [[key] + ([0] * (50))], columns=['word'] + [f'df{i}' for i in range(1, 50 + 1)]), ignore_index=True)

        for index, (key, value) in enumerate(count_dict.items()):

            for doc, count in value.items():

                df.at[index, f'df{doc}'] = np.float32(1 + math.log(count))

        df.to_csv("./dist/tf.csv")


class DocumentInverseFrequency():

    short_stories_len = os.listdir(os.path.abspath('.') + "/dist/ShortStories")

    def __init__(self, path_to_tf_csv: str = os.path.abspath('.') + "/dist/tf.csv"):
        self.path_to_tf_csv = path_to_tf_csv
        self.document_columns = [f'df{i}' for i in range(1, 50 + 1)]
        self.path_to_idf_csv = './dist/idf.csv'

    def BuildInverseDocumentFrequency(self):

        tf_df = pd.read_csv(self.path_to_tf_csv).reset_index(drop=True)

        del tf_df['Unnamed: 0']

        tf_df['idf'] = pd.DataFrame(
            [0] * len(tf_df), columns=['idf'], dtype=np.float32)

        for i in range(0, len(tf_df)):
            df_i = 0
            for document in self.document_columns:
                if tf_df.iloc[i][document] != 0:
                    df_i += 1

            tf_df.at[i, 'idf'] = np.float32(
                math.log(np.float32(len(self.short_stories_len)/df_i)))

        tf_df.to_csv(self.path_to_idf_csv)


class TFBindIDF():

    def __init__(self):
        self.idf_doc_path = './dist/idf.csv'
        self.tf_idf_save_pd_path = './dist/tf-idf.csv'
        self.document_names = [f"df{i}" for i in range(1, 50 + 1)]

    def BuildTFAndIDF(self):

        df = pd.DataFrame(
            columns=self.document_names)

        tf_idf = pd.read_csv(self.idf_doc_path).reset_index(drop=True)

        for index in range(0, len(tf_idf)):
            idf_value = list(tf_idf.iloc[index, 2:53])[-1]
            df_values = list(tf_idf.iloc[index, 2:52])

            new_tf_id = []
            for i in range(0, len(df_values)):
                new_tf_id.append(df_values[i] * idf_value)

            new_tf_id = list(tf_idf.iloc[index, 1:2]) + new_tf_id + [idf_value]

            df = df.append(pd.DataFrame([new_tf_id], columns=[
                'word'] + self.document_names + ['idf']), ignore_index=True)

        df = self.NormalizeVectors(df)

        df.to_csv(self.tf_idf_save_pd_path)

    def NormalizeVectors(self, df: pd.DataFrame):

        __temp_df = df.copy()

        # For each column
        for document in self.document_names:
            __temp_df[document] = __temp_df[document] / \
                np.linalg.norm(__temp_df[document])

        return __temp_df


class VectorSpaceModel():

    '''
    This class is responsible for maintaining the Vector Space Model which
    will act for the following responsibilites,

    1. Keep an in memory dataframe of the tf-idf matrix
    2. Performing cosine similarity with a given query
    3. Maintaining the weighting scheme for the tf matrix
    4. Normalizing for cosine similarity
    '''

    def __init__(self, alpha = 10e-8, path_for_tf_idf_df: str = './dist/tf-idf.csv'):
        self.path_for_tf_idf_df = path_for_tf_idf_df
        self.tf_idf_df = pd.read_csv(self.path_for_tf_idf_df)
        self.alpha = alpha

    def GetQueryDocs(self):
        pass

    def ProcessQuery(self, query: str):

        Preprocessing = AuxPreprocessing()
        return Preprocessing.PreprocessQuery(query)

    def GenerateQueryVector(self, query: str):

        data = self.ProcessQuery(query)

        data_dict = {}

        for token in data:
            if token not in data_dict:
                data_dict[token] = 1
            else:
                data_dict[token] += 1

        query_words = {token: 0 for token in list(self.tf_idf_df['word'])}

        for key, value in data_dict.items():
            if key in query_words:
                query_words[key] = value

        total_sum = 0
        for key, value in query_words.items():
            total_sum += value

        if total_sum != 0:
            for key, value in query_words.items():
                query_words[key] = (value / total_sum)

        query_dist = 0

        for key, value in query_words.items():
            query_dist += (value**2)

        final_ranking = {}

        for doc_index in range(1, 50 + 1):
            word_dict, df_dict = self.tf_idf_df['word'].to_dict(
            ), self.tf_idf_df[f'df{doc_index}'].to_dict()

            doc_dict = {}
            for (_, word_value), (_, df_value) in zip(word_dict.items(), df_dict.items()):
                doc_dict[word_value] = df_value

            doc_dist = 0

            for _, value in doc_dict.items():
                doc_dist += (value**2)

            dot_product = 0

            for (_, query_tf), (_, doc_tf) in zip(query_words.items(), doc_dict.items()):
                dot_product += (query_tf * doc_tf)

            if query_dist != 0 and doc_dist != 0:
                final_ranking[f"df{doc_index}"] = dot_product / \
                    (math.pow(query_dist, 1/3) * math.pow(doc_dist, 1/3))
            else:
                final_ranking[f'df{doc_index}'] = 0

        return final_ranking

    def ComplexQuery(self, query: str):

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

        if len(final_phrases) == 0:
            raise Exception("Invalid query")

        final_doc_results.append(self.GenerateQueryVector(final_phrases[0]))

        if len(operators) > 1 and operators[0] == 'not':
            final_doc_results[0] = self.InvertRankedQuery(
                self.GenerateQueryVector(final_phrases[0]))
            operators.pop(0)

        # No other operators involved and a single token
        if len(final_phrases) == 1:

            return self.CleanDict(final_doc_results[0].items())

        elif len(operators) + 1 == len(final_phrases) and 'not' not in operators:

            query_results.append(final_doc_results[0])

            for i in range(1, len(final_phrases)):
                final_doc_results.append(
                    self.GenerateQueryVector(final_phrases[i]))

            for i in range(0, len(operators)):
                query_results.append(self.QueryBoolHandler(
                    query_results[i], final_doc_results[i], operators[i]))

            return self.CleanDict(query_results[-1].items())

        elif len(operators) + 1 == len(final_phrases) and 'not' in operators:

            raise Exception("Invalid query")

        elif len(operators) >= len(final_phrases):

            if len(operators) - operators.count('not') + 1 != len(final_phrases):

                raise Exception("Invalid query")

            '''
            First operator will never be not thanks to checking for the operator length 2 control flows above
            '''

            new_operators = []
            phrase_iterator = 0

            for idx in range(0, len(operators)):

                try:
                    if operators[idx] == 'not':

                        if operators[idx - 1] == 'not':
                            final_doc_results[-1] = self.InvertRankedQuery(
                                final_doc_results[-1])
                        else:
                            final_doc_results.append(self.InvertRankedQuery(
                                self.GenerateQueryVector(final_phrases[phrase_iterator])))

                    else:
                        phrase_iterator += 1
                        new_operators.append(operators[idx])
                except IndexError:
                    raise Exception(f"Invalid indexing, {idx}")

            query_results.append(final_doc_results[0])

            for i in range(0, len(new_operators)):
                query_results.append(self.QueryBoolHandler(
                    query_results[i], final_doc_results[i + 1], operators[i]))

            return self.CleanDict(query_results[-1].items())

    def ORQuery(self, df1: dict, df2: dict):
        return {k: (v1 + v2) for (k, v1), (_, v2) in zip(df1.items(), df2.items())}

    def ANDQuery(self, df1: dict, df2: dict):
        return {k: (v1 * v2) for (k, v1), (_, v2) in zip(df1.items(), df2.items())}

    def QueryBoolHandler(self, df1: dict, df2: dict, operator: str):
        if operator == 'and':
            return self.ANDQuery(df1, df2)
        elif operator == 'or':
            return self.ORQuery(df1, df2)

    def InvertRankedQuery(self, df_dict: dict):

        __auto_df_dict = df_dict.copy()

        zero_count = 0
        for key, value in __auto_df_dict.items():
            if value == 0:
                zero_count += 1
            else:
                __auto_df_dict[key] = -1

        equal_prob = np.float32(zero_count / 50)

        for key, value in __auto_df_dict.items():
            if value == 0:
                __auto_df_dict[key] = equal_prob
            elif value == -1:
                __auto_df_dict[key] = 0

        return __auto_df_dict

    def CleanDict(self, dict_to_clean: dict):

        new_dict = dict(
            filter(lambda item: item[1] != 0 and item[1] >= self.alpha, dict_to_clean))

        return {k: v for k, v in sorted(new_dict.items(), reverse=True, key=lambda item: item[1])}
