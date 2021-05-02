# Vector Space Model, and sub components for tf, idf, and tf-idf
from VectorSpaceModel import VectorSpaceModel, TermFrequencyIndexer, DocumentInverseFrequency, TFBindIDF

'''Gold standard queries as mentioned in ../data/ShortStories.txt'''
gold_standard_queries = ['beard',
                         'passenger',
                         'permission and possible',
                         'power and play',
                         'ladies and gentleman',
                         'strange and land and play',
                         'god and man and play',
                         'smiling face /3',
                         'filling room /1',
                         'not pleaser and not fever'
                         ]

'''The respective outputs of the gold standard queries'''
query_result_checks = [
    ['1', '2', '4', '6', '11', '20', '21', '23', '25', '26', '31', '34', '44'],
    ['2', '5', '19', '41', '43'],
    ['45'],
    ['2'],
    ['2', '16', '26', '36', '48'],
    ['49'],
    ['1', '2', '4', '7', '16', '19', '22', '23',
        '24', '25', '26', '28', '38', '46'],
    ['11'],
    ['21'],
    ['3', '4', '5', '6', '7', '8', '9', '10', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26',
        '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '39', '40', '41', '42', '44', '45', '46', '47', '48', '49', '50']
]

'''Text meant to help for checking if the preprocessing steps are working as expected'''
test_query_unpreprocessed = 'chimney is tumbling down, the steps at the front-door are rotting away and overgrown with grass, and there are only traces left of the stucco. The front of the lodge faces the hospital; at the back it looks out into the open country, from which it is separated by the grey hospital fence with nails on it. These nails, with their points upwards, and the fence, and the lodge itself, have that peculiar, desolate, God-forsaken look which is only found in our hospital and prison buildings.'

'''Processed text to help in checking if the indexes are being properly built'''
test_query_preprocessed = 'dissolut furtiv moistur encount sunlight marbl slab dug sunni acacia acacia acacia acacia acacia acacia acacia acacia acacia acacia acacia acacia acacia acacia acacia'

# Uncomment the lines below to build the term frequency matrix with the respective words
# The below two lines generate the ../dist/tf.csv
# tf = TermFrequencyIndexer()
# tf.IndexShortStories()

# Uncomment the lines below to build the inverse document frequency matrix with the respective words
# The below two lines generate the ../dist/idf.csv
# idf = DocumentInverseFrequency()
# idf.BuildInverseDocumentFrequency()

# Uncomment the lines below to use the idf with the tf to generate a new matrix
# Results in the creation of the ../dist/tf-idf.csv
# tf_idf = TFBindIDF()
# tf_idf.BuildTFAndIDF()

'''
Create an object for the Vector Space Model
It should take two parameters, first for the alpha ( set to 10e-8 ), and 
the second as the path to the ShortStories folder
'''
VSM = VectorSpaceModel()

# Traversing through all of the gold standard queries
for idx, query in enumerate(gold_standard_queries):

    try:

        # If encounter a proximity query, continue to
        # next iteration
        if '/' in query:
            continue
        # Else, retrieve results for the given complex query
        else:
            query_results = VSM.ComplexQuery(query)

        # Preprocess keys of the format "df{index}" to reduce
        # it to just "{index}". The index represents the filename
        query_results = [key[2:] for key in query_results.keys()]

        # Checking if all the relevant docs have been retrieved
        # as per the test case
        correct, not_found_docs, false_positives = True, [], []

        # For every list in the gold standard check list ...
        for query_check in query_result_checks[idx]:

            # ... if we encounter a doc not retrieved by
            # our model in the query_results ...
            if query_check not in query_results:

                # ... then set the correct flag to False ...
                correct = False

                # ... Add to a list the total documents that
                # were not found by our model
                not_found_docs.append(query_check)

        # Finally, print the results of the query
        print(f"Query: \"{query}\",\nResult: ", end="")

        # If all the required results were retrieved, print true
        if correct:
            print(f"\"True\"\n")

        # Else, print False ...
        else:
            print(f"\"False\"")

            # ... and mention the docs that were not found ...
            print(f"Docs not found were, {not_found_docs}\n")

    # If a query of unknown format is encountered that cannot be indexed ...
    except IndexError as error:

        # ... throw an error
        print(f"Error thrown due to query: {query}. Error is, \"{error}\"")
