from BooleanRetrievalModel import BooleanRetrievalModel
from Preprocessing import IndexPreprocessing, Preprocessing, AuxPreprocessing
from VectorSpaceModel import VectorSpaceModel, TermFrequencyIndexer, DocumentInverseFrequency, TFBindIDF

### FOR BOOLEAN PROCESSING
# # TOTAL WORDS GENERATION
# preprocess = Preprocessing()
# preprocess.data_load_and_save()

# # INDEX PROCESSING
# preprocess = IndexPreprocessing()
# preprocess.process_data_through_pipelines()
# preprocess.get_saved_normalized_words()

# model = BooleanRetrievalModel()

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

test_query_unpreprocessed = 'chimney is tumbling down, the steps at the front-door are rotting away and overgrown with grass, and there are only traces left of the stucco. The front of the lodge faces the hospital; at the back it looks out into the open country, from which it is separated by the grey hospital fence with nails on it. These nails, with their points upwards, and the fence, and the lodge itself, have that peculiar, desolate, God-forsaken look which is only found in our hospital and prison buildings.'

test_query_preprocessed = 'dissolut furtiv moistur encount sunlight marbl slab dug sunni acacia acacia acacia acacia acacia acacia acacia acacia acacia acacia acacia acacia acacia acacia acacia'

# tf = TermFrequencyIndexer()
# tf.IndexShortStories()

# idf = DocumentInverseFrequency()
# idf.BuildInverseDocumentFrequency()

# tf_idf = TFBindIDF()
# tf_idf.BuildTFAndIDF()

VSM = VectorSpaceModel()

# print("CODE LEFT TO WRITE FOR FALSE POSITIVES\n\n\n")

for idx, query in enumerate(gold_standard_queries):

    try:
        if '/' in query:
            continue
        else:
            query_results = VSM.ComplexQuery(query)

        query_results = [key[2:] for key in query_results.keys()]

        correct, not_found_docs, false_positives = True, [], []
        for query_check in query_result_checks[idx]:
            if query_check not in query_results:
                correct = False
                not_found_docs.append(query_check)

        print(f"Query: \"{query}\",\nResult: ", end="")

        if correct:
            print(f"\"True\"\n")

        else:
            print(f"\"False\"")
            print(f"Docs not found were, {not_found_docs}\n")

    except IndexError as error:
        print(f"Error thrown due to query: {query}. Error is, \"{error}\"")
