from BooleanRetrievalModel import BooleanRetrievalModel
from Preprocessing import IndexPreprocessing, Preprocessing

# # TOTAL WORDS GENERATION
# preprocess = Preprocessing()
# preprocess.data_load_and_save()

# # INDEX PROCESSING
# preprocess = IndexPreprocessing()
# preprocess.process_data_through_pipelines()
# preprocess.get_saved_normalized_words()

model = BooleanRetrievalModel()

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

print("CODE LEFT TO WRITE FOR FALSE POSITIVES\n\n\n")

for idx, query in enumerate(gold_standard_queries):

    try:
        if '/' in query:
            query_results = model.ProximityQuery(query)
        else:
            query_results = model.ComplexBooleanQuery(query)

        if type(query_results[0]) == int:
            query_results = [str(results) for results in query_results]

        correct, not_found_docs, false_positives = True, [], []
        for query_check in query_result_checks[idx]:
            if query_check not in query_results:
                correct = False
                not_found_docs.append(query_check)

        # BUGGY!
        # for false_positive_check in query_result_checks:
        #     for check in false_positive_check:
        #         if check not in query_results:
        #             false_positives.append(check)

        print(f"Query: \"{query}\",\nResult: ", end="")

        if correct:
            print(f"\"True\"\n")

            # if len(false_positives) != 0:
            #     print(f"False positive detected as the following, {false_positives}")
        else:
            print(f"\"False\"\n")
            print(f"Docs not found were, {not_found_docs}")

    except IndexError as error:
        print(f"Error thrown due to query: {query}. Error is, \"{error}\"")
