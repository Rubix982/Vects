# AuxPreprocessing required to use the process pipeline for the
# input queries
from Preprocessing import AuxPreprocessing

# Pandas to handle dataframes
import pandas as pd

# Numpy for datatype and normalization
import numpy as np

# Math for sqrt and log operations
import math

# OS for local file reading and writing
import os


class TermFrequencyIndexer():

    '''
    This class is responsible for building the
    ../dist/tf.csv file. The file 'tf.csv' contains
    the sparse matrix of the term frequencies
    as indexed properly by the given unique
    documents in the ../dist/ShortStories folder
    '''

    '''Gobal variable defining the complete path for the ShortStories folder'''
    short_stories_path = os.path.abspath('.') + "/dist/ShortStories"

    def __init__(self, list_of_filenames: list = os.listdir(short_stories_path)):
        '''
        This is the function called on initialization of
        TermFrequencyIndexer

        Args:
            self: The object itself.
            list_of_filenames: The complete list of files
            under the ShortStories folder, unless specified elsewhere

        Returns:
            The newly object created
        '''

        self.list_of_filenames = list_of_filenames

    def IndexShortStories(self):
        '''
        Responsible for the actual indexing

        Args:
            self: The object itself
        Returns:
            None

        Raises:
            None: No exceptions
        '''

        # Creates a dataframe to hold all the data together
        # generates the columns ['word', 'df1', 'df2', 'df3', 'df4' ...]
        # Where df is just a shorthand for one dataframe
        df = pd.DataFrame(
            columns=['word'] + [f'df{i}' for i in range(1, 50 + 1)])

        # Counting dictionary, responsible for the frequency
        count_dict = {}

        # Traversing through the list of files ...
        for filename in self.list_of_filenames:

            # ... Open each file in the readable mode, set fd as file ...
            with open(self.short_stories_path + "/" + filename, mode='r') as file:

                # ... Read the entire data in a local variable, first
                # split on spacing ...
                data = str(file.read()).split(' ')

                # ... Retrieve the index of the file ...
                index = filename.split('.')[0]

                # ... Traversing through all the tokens in the data
                # variable ...
                for token in data:

                    # ... If a token does not occur in the count_dictionary ...
                    if token not in count_dict:

                        # ... Create an empty object ...
                        count_dict[token] = {}

                        # ...Create a key 'index' in that object, equate
                        # it to one, for a first appearence
                        count_dict[token][index] = 1

                    # Else if the key already exists beforehand
                    else:

                        # For some reason, this prevents something from breaking
                        # It was some key error
                        # I'm not sure why that error was ocurring. I don't think
                        # I could think of a valid reason
                        if index not in count_dict[token]:

                            # Create index, equate to zero
                            count_dict[token][index] = 0

                        # Accumalate the frequencies of the new index
                        count_dict[token][index] += 1

        # Traversing through all of the keys in the dataframe
        for key, _ in count_dict.items():

            # Append newer rows as DataFrames, each row with a unique word
            df = df.append(pd.DataFrame(
                [[key] + ([0] * (50))], columns=['word'] + [f'df{i}' for i in range(1, 50 + 1)]), ignore_index=True)

        # Finally, for the actually frequency
        for index, (key, value) in enumerate(count_dict.items()):

            # Retrieve the document index, and the count of that document
            for doc, count in value.items():

                # Using '1 + log(tf)' instead for optimization reasons
                df.at[index, f'df{doc}'] = np.float32(1 + math.log(count))

        # Store to local disk
        df.to_csv("./dist/tf.csv")


class DocumentInverseFrequency():

    '''
    This class is responsible for building the
    ../dist/idf.csv file. The file 'idf.csv' contains
    the sparse matrix of the term frequencies
    as indexed properly by the given unique
    documents in the ../dist/ShortStories folder
    '''

    '''Gobal variable defining the complete path for the ShortStories folder'''
    short_stories_len = os.listdir(os.path.abspath('.') + "/dist/ShortStories")

    def __init__(self, path_to_tf_csv: str = os.path.abspath('.') + "/dist/tf.csv"):
        ''''
        This is the function called on initialiation of DocumentInverseFrequency

        Args:
            path_to_tf_csv: Path to the tf.csv file. Default keyword assumed
            document_columns: The list of columns for the dataframe
            path_to_idf_csv: Where the dafaframe will be finally stored

        Returns:
            Returns the newly created object

        Raises:
            None: No exception
        ''''
        self.path_to_tf_csv = path_to_tf_csv
        self.document_columns = [f'df{i}' for i in range(1, 50 + 1)]
        self.path_to_idf_csv = './dist/idf.csv'

    def BuildInverseDocumentFrequency(self):
        '''
        this function is responsible for building the inverse
        document frequency

        Args:
            self: The object itself.

        Returns:
            TNone, it creates a new document on the local hard disk

        Raises:
            None: No exceptions
        '''

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
        '''
        This class is responsible for building the
        ../dist/tf-idf.csv file. The file 'tf-idf.csv' contains
        the sparse matrix of the term frequencies
        multiplied by the inverse document frequencies from 'idf.csv'
        '''

    def __init__(self):

        '''
        This is the function called on initialization of 
        TFBindIDF

        Args:
            self: The object itself.

        Returns:
            The newly object created
        '''

        # Path to idf.csv file
        self.idf_doc_path = './dist/idf.csv'
        
        # Path to the to-be-saved tf-idf.csv
        self.tf_idf_save_pd_path = './dist/tf-idf.csv'
        
        # List to contain the name of the documents
        self.document_names = [f"df{i}" for i in range(1, 50 + 1)]

    def BuildTFAndIDF(self):

        '''
        This function is responsible for actually
        building the tf-idf.csv

        Args:
            self: the object itself

        Returns:
            None. It saves tf-idf.csv to the local hard disk

        Raises:
            None: No exceptions
        '''        

        # Creates a new dataframe consisting only of the document names
        df = pd.DataFrame(
            columns=self.document_names)

        # Reads the local idf.csv file, set reset_index(drop=True)
        tf_idf = pd.read_csv(self.idf_doc_path).reset_index(drop=True)

        # Traversing through all of the dataframe
        for index in range(0, len(tf_idf)):

            # Extracing the idf values
            idf_value = list(tf_idf.iloc[index, 2:53])[-1]
            
            # Extracting the df values
            df_values = list(tf_idf.iloc[index, 2:52])

            # Creating a new list to contain the tf_id(s)
            new_tf_id = []

            # Going through all of the df values in the rows
            for i in range(0, len(df_values)):

                # Multiplying the df_values with the idf
                new_tf_id.append(df_values[i] * idf_value)

            # Creating a new row item for the dataframe
            new_tf_id = list(tf_idf.iloc[index, 1:2]) + new_tf_id + [idf_value]

            # Appending to the new dataframe
            df = df.append(pd.DataFrame([new_tf_id], columns=[
                'word'] + self.document_names + ['idf']), ignore_index=True)

        # Normalizing the vectors in the dataframe
        df = self.NormalizeVectors(df)

        # Saving to the local hard disk
        df.to_csv(self.tf_idf_save_pd_path)

    def NormalizeVectors(self, df: pd.DataFrame):

        '''
        This function is responsible for normalizing
        the individual vectors in the tf idf matrix

        Args:
            df: This the dataframe to normalize

        Returns:
            Returns a new dataframe with normalized vectors

        Raises:
            None: No Exception
        '''

        # Create a local copy of the dataframe
        __temp_df = df.copy()

        # For each column in the document names
        for document in self.document_names:

            '''
            Set each vector to a normalized form of it self by
            diving the vector with the norm of that vector
            '''
            __temp_df[document] = __temp_df[document] / \
                np.linalg.norm(__temp_df[document])

        # Return the new normalized dataframe
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

    def __init__(self, alpha=10e-8, path_for_tf_idf_df: str = './dist/tf-idf.csv'):

        '''
        This is the function called on initialization of
        TermFrequencyIndexer

        Args:
            self: The object itself.
            alpha: The cutoff value for filtering purposes
            path_for_tf_idf_df: The path to the tf-idf.csv

        Returns:
            The newly object created
        '''

        # Sets the path to find the 'tf-idf.csv'
        self.path_for_tf_idf_df = path_for_tf_idf_df

        # Reads the file locally for the 'tf-idf.csv'
        self.tf_idf_df = pd.read_csv(self.path_for_tf_idf_df)
        
        # Sets the cut off value for filtering
        self.alpha = alpha

    def ProcessQuery(self, query: str):

        '''
        This function has a pipeline for preprocessing the stringss.

        Args:
            self: The object itself
            query: The string to be preprocessed

        Returns:
            The string, but preprocessed

        Raises:
            None: No expcetion
        '''

        Preprocessing = AuxPreprocessing()
        return Preprocessing.PreprocessQuery(query)

    def GenerateQueryVector(self, query: str):

        '''
        This function is responsible for generating query vectors
        for each of the documents, along with their ranked scores

        Args:
            self: The object itself
            query: The query to be parsed
        
        Returns:
            A dictionary with the doc iterations as their keys, and
            their ranking as values
        
        Raises:
            None: No exceptions
        '''

        # Preprocess the query first
        data = self.ProcessQuery(query)

        # Create a dictionary
        data_dict = {}

        # This seems redundant couple with the next for loop
        # below this loop, but it basically stores the 
        # frequency of the terms in the query
        for token in data:
            if token not in data_dict:
                data_dict[token] = 1
            else:
                data_dict[token] += 1

        # Then we generate a dictionary of all the keywords within our
        # dataframe, and set each key's value to 0
        query_words = {token: 0 for token in list(self.tf_idf_df['word'])}

        # Traversing through the dictionary of items
        for key, value in data_dict.items():

            # Checking is key is in the list of query_words
            if key in query_words:

                # Storing the resultant answer
                query_words[key] = value

        # Create a list to store all the values
        total_sum = []
        
        # Traversing through the query dictionary
        for key, value in query_words.items():

            # Appending to our aforementioned list
            total_sum.append(value)

        # If the total sum is not found to be empty
        if total_sum != []:

            # Traverse through the keys in the query word
            # dictionary
            for key, value in query_words.items():
                
                # Set each key to the normalized form of it's former
                # value
                query_words[key] = (value / np.linalg.norm(total_sum))

        # Setting the query_dist to 0, meant to
        # represnet |q|
        query_dist = 0

        # For each key value pair in query_words ...
        for key, value in query_words.items():

            # We square and add the result to somewhere
            query_dist += (value**2)

        # For the final ranking, we first create a dictionary
        final_ranking = {}

        # Traversing through the entire doc index
        for doc_index in range(1, 50 + 1):

            # Extracing the word series and our respective {doc_index}
            # series from the dataframe
            word_dict, df_dict = self.tf_idf_df['word'].to_dict(
            ), self.tf_idf_df[f'df{doc_index}'].to_dict()

            # Creating a doc to handle and deal with the
            # new doc dict to parse 
            doc_dict = {}

            # Using our two above dicts, we combine the results to store
            # more concisely. Previously, the indexes in the
            # original datafame acted as keys, so we ignore them here
            for (_, word_value), (_, df_value) in zip(word_dict.items(), df_dict.items()):

                # Setting the word ( key ) to the df_value ( value )
                doc_dict[word_value] = df_value

            # Setting the doc_dist to 0, this is meant to
            # repesent |d|
            doc_dist = 0

            # Again, like we did for the query, we do the same
            # for the doc
            for _, value in doc_dict.items():
                doc_dist += (value**2)

            # Creating a variable for the dot_product
            dot_product = 0

            # For the numerator section of the cosine similarity
            for (_, query_tf), (_, doc_tf) in zip(query_words.items(), doc_dict.items()):
                dot_product += (query_tf * doc_tf)

            # If there is indeed some value in both 
            # the normalized forms
            if query_dist != 0 and doc_dist != 0:
                
                # We assign the finalranking dict to this cosine
                # similarity score
                final_ranking[f"df{doc_index}"] = dot_product / \
                    (math.pow(query_dist, 1/3) * math.pow(doc_dist, 1/3))
            else:

                # If there is a single 0, we simply assign 0 here
                final_ranking[f'df{doc_index}'] = 0

        # Now, we return the final ranking
        return final_ranking

    def ComplexQuery(self, query: str, alpha: float = 10e-8):

        """
        This is an example of Google style.

        Args:
            query: The query to be parsed 
            alpha: The threshold filter value

        Returns:
            A dictionary with the docs as keys, their ranking scores as values

        Raises:
            Exception: Invalid query
        """

        # Initializing all variables for creation of final 
        # ranking dictionary
        phrases, operators, init_pos, final_phrases, final_doc_results, query_results, __tokens = [
        ], [], 0, [], [], [], [token.lower() for token in query.strip(' ').split(' ')]

        # Check for correct syntax
        for i in range(0, len(__tokens) - 1):
            if (__tokens[i] == 'or' and __tokens[i + 1] == 'or') or \
                (__tokens[i] == 'and' and __tokens[i + 1] == 'and') or \
                    __tokens[i] == 'not' and __tokens[i + 1] == 'not':
                return "Invalid query structure!"

        # Enumerating the indexed tokens
        for index, token in enumerate(__tokens):
            
            # Checking if we come across an operator
            if token == 'and' or token == 'or' or token == 'not':
                
                # Appending the phrases so far
                phrases.append(__tokens[init_pos:index])
                
                # Changing the init position
                init_pos = index + 1

                # Appending the operators
                operators.append(token)

            # If we come across the last phrase
            if index + 1 == len(__tokens):

                # Appending the last token
                phrases.append(str(__tokens[-1]))

        # Traversing through each phrase
        for phrase in phrases:

            # If the phase is not empty
            if phrase != []:

                if type(phrase) is list and len(phrase) == 1:
                    
                    # Removing extra layered list
                    final_phrases.append(phrase[0])
                else:

                    # Appending the phrase normally
                    final_phrases.append(phrase)

        # Preprocessing the operators list
        operators = [operator for operator in operators if operator != []]

        # If no phrases were captured
        if len(final_phrases) == 0:

            # Raise exception
            raise Exception("Invalid query")

        # Appending to the final list of docs by generating the appropriate
        # query vector
        final_doc_results.append(self.GenerateQueryVector(final_phrases[0]))

        # If more than one operators exist, and the first one is 'not'
        if len(operators) > 1 and operators[0] == 'not':

            # Store the first query vector
            final_doc_results[0] = self.InvertRankedQuery(
                self.GenerateQueryVector(final_phrases[0]))

            # Remove the first operator
            operators.pop(0)

        # No other operators involved and a single token
        if len(final_phrases) == 1:

            # Simply returned a 'cleaned' dict
            return self.CleanDict(final_doc_results[0].items(), alpha)

        # Else if more than one operators exist, and it is the right structure
        elif len(operators) + 1 == len(final_phrases) and 'not' not in operators:

            # Append to query results the first 
            # final_doc_results
            query_results.append(final_doc_results[0])

            # Traversing through the whole of the 
            # final phrases
            for i in range(1, len(final_phrases)):
                
                # We first append the result of the
                # vector query that is generated
                final_doc_results.append(
                    self.GenerateQueryVector(final_phrases[i]))

            # We then got through the list of operators 
            # once we have a structure format of the
            # new phrase and operator format
            for i in range(0, len(operators)):
                
                # Append to query_results a result from the
                # QueryBoolHandler and the operator
                query_results.append(self.QueryBoolHandler(
                    query_results[i], final_doc_results[i], operators[i]))

            # Return a 'cleaned' dict
            return self.CleanDict(query_results[-1].items(), alpha)

        # Elise if there still exist nots, and the structure isn't proper
        elif len(operators) + 1 == len(final_phrases) and 'not' in operators:

            # We raise an exception
            raise Exception("Invalid query")

        # If there are more operators than the phrases, then there are 
        # obvious 'not'(s) in the operators list
        elif len(operators) >= len(final_phrases):

            # If removing the nots still does not give us a 
            # proper query format ...
            if len(operators) - operators.count('not') + 1 != len(final_phrases):

                # ... raise an exception
                raise Exception("Invalid query")

            '''
            First operator will never be not thanks to checking for the operator length 2 control flows above
            '''

            # variable to store the new operators
            new_operators = []

            # Iterating through the phase
            phrase_iterator = 0

            # Going through each of the operators
            for idx in range(0, len(operators)):

                # USing a try clause
                try:
                    
                    # if we come across a not in the operator list
                    if operators[idx] == 'not':

                        # ... and the previou operator was also not
                        if operators[idx - 1] == 'not':

                            # We just invert the results
                            final_doc_results[-1] = self.InvertRankedQuery(
                                final_doc_results[-1])
                        
                        # ... else ...
                        else:

                            # We append to final_doc_results a new inverted result
                            # generated from GenerateQueryVector
                            final_doc_results.append(self.InvertRankedQuery(
                                self.GenerateQueryVector(final_phrases[phrase_iterator])))

                    # If we don't encounter a 'not' operators
                    else:

                        # Just incremenet the phrase_iterator
                        phrase_iterator += 1

                        # And append the operator to the new_operators list
                        new_operators.append(operators[idx])

                # Display indexing error, if it occurs
                except IndexError:

                    # Raise invalid indexing error
                    raise Exception(f"Invalid indexing, {idx}")

            # Append the last results to query_results
            query_results.append(final_doc_results[0])

            # going through each of the new operators
            for i in range(0, len(new_operators)):

                # We do the same thing as the above
                query_results.append(self.QueryBoolHandler(
                    query_results[i], final_doc_results[i + 1], operators[i]))

            # We now return a 'cleaned' dict
            return self.CleanDict(query_results[-1].items(), alpha)

    def ORQuery(self, df1: dict, df2: dict):
        ''''
        This handles the OR operator

        Args:
            df1: First dict of information.
            df2: Second dict of information

        Returns:
            A dict that has the OR operation performed on it

        Raises:
            None: No exception
        ''''

        return {k: (v1 + v2) for (k, v1), (_, v2) in zip(df1.items(), df2.items())}

    def ANDQuery(self, df1: dict, df2: dict):
        ''''
        This handles the AND operator

        Args:
            df1: First dict of information.
            df2: Second dict of information

        Returns:
            A dict that has the AND operation performed on it

        Raises:
            None: No exception
        ''''

        return {k: (v1 * v2) for (k, v1), (_, v2) in zip(df1.items(), df2.items())}

    def QueryBoolHandler(self, df1: dict, df2: dict, operator: str):
        ''''
        TThis handles both the operator logic

        Args:
            df1: First dict of information.
            df2: Second dict of information
            operator: The operator specified

        Returns:
            Dict with specified operation performed on it

        Raises:
            None: No exception
        ''''
        if operator == 'and':
            return self.ANDQuery(df1, df2)
        elif operator == 'or':
            return self.ORQuery(df1, df2)

    def InvertRankedQuery(self, df_dict: dict):
        ''''
        This inverts the ranked query

        Args:
            df_dict: Inverts a dict

        Returns:
            A dict that has the NOT operation performed on it

        Raises:
            None: No exception
        ''''

        # Make local, temporary dict
        __auto_df_dict = df_dict.copy()

        # For counting the number of zeroes
        zero_count = 0

        # Traversing through each of the local dict items
        for key, value in __auto_df_dict.items():

            # if we encounter a zero value
            if value == 0:

                # Increment!
                zero_count += 1
            else:

                # If it was not zero, set to a value
                # it can't possible be beforehand, that is,
                # -1, to mark it's previous history
                __auto_df_dict[key] = -1

        # determine the equal probability
        equal_prob = np.float32(zero_count / 50)

        # Traversing through each of the dict items
        for key, value in __auto_df_dict.items():

            # If value is 0
            if value == 0:

                # set local dict to be equal to equal_prob
                __auto_df_dict[key] = equal_prob
            
            # Elise if value is -1
            elif value == -1:

                # Set dict to equate to 0
                __auto_df_dict[key] = 0

        # Return newly created dict
        return __auto_df_dict

    def CleanDict(self, dict_to_clean: dict, alpha: float):

        ''''
        This cleans a dict, which just removes keys with 0 values,
        and filters using the threshold value

        Args:
            dict_to_clean: The dict to clean
            alpha: The alpha threshold

        Returns:
            A sorted, filtered dictionary

        Raises:
            None: No exception
        ''''

        new_dict = dict(
            filter(lambda item: item[1] != 0 and item[1] >= alpha, dict_to_clean))

        return {k: v for k, v in sorted(new_dict.items(), reverse=True, key=lambda item: item[1])}
