import pandas as pd


class VectorSpaceModel():

    '''
    This class is responsible for maintaining the Vector Space Model which
    will act for the following responsibilites,

    1. Keep an in memory dataframe of the tf-idf matrix
    2. Performing cosine similarity with a given query
    3. Maintaining the weighting scheme for the tf matrix
    4. Normalizing for cosine similarity
    '''

    def __init__(self, path_for_tf_idf_df: str = './dist/tf-idf.csv'):
        self.path_for_tf_idf_df = path_for_tf_idf_df
        self.tf_idf_df = pd.read_csv(self.path_for_tf_idf_df)

    def GetQueryDocs(self):
        pass

    def GenerateQueryVector(self, query: str):
        
        data = query.split(" ")
        data_dict = {}

        for token in data:
            if token not in data_dict:
                data_dict[token] = 1
            else:
                data_dict[token] += 1

        total_words = list(self.tf_idf_df['word'])
        
        