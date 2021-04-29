#!/usr/bin/env python3

import pathlib
import os
import string
import nltk
import json
import re

import multiprocessing as mp

# NLTK
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer


class InvertedIndex:

    def __init__(self, word, dict_str):
        self.word = word
        self.dict_str = dict_str


class PositionNode():

    def __init__(self, doc_id: str, position_list: list):
        self.doc_id = doc_id
        self.position_list = position_list


class PositionalIndex():

    def __init__(self, unique_hash):
        self.unique_hash = unique_hash
        self.document_listing_positions = ''


class AuxPreprocessing(object):

    def __init__(self):
        pass

    @staticmethod
    def Tokenizer(line: str,
                  nltk_tokenizer: nltk.RegexpTokenizer,
                  stop_words_list: list):

        # TOKENIZATION - removes punctuation!
        tokens = nltk_tokenizer.tokenize(line)

        # CASE FOLDING
        tokens = [token.lower() for token in tokens]

        # STOP WORDS REMOVAL
        for token in tokens:
            if token in stop_words_list:
                tokens.remove(token)

        return tokens

    @staticmethod
    def Stemmer(tokens: list,
                stemming_func: PorterStemmer):

        return [stemming_func.stem(token) for token in tokens]

    @staticmethod
    def Lemmatize_func(tokens: list,
                       lemmatizer: WordNetLemmatizer):
        return [lemmatizer.lemmatize(token) for token in tokens]


class Porter(object):

    def __init__(self):
        pass

    @staticmethod
    def CustomPorterAlgorithm(input_str: str):

        # PREPROCESSING
        input_str = input_str.lower()

        # VARIABLE SECTION
        '''
        USED IN STEP 1A
        '''
        from_str = ['sess', 'ies', 'ss', 's']
        to_str = ['ss', 'i', 'ss', '']

        '''
        USED IN STEP 1B
        '''
        vowel_list = ['a', 'e', 'i', 'o', 'u']

        '''
        USED IN STEP 2
        '''
        from_suffix_consideration = ['ational', 'tional', 'enci', 'izer', 'abli', 'alli', 'entli', 'ousli', 'ization',
                                     'ation', 'ator', 'alism', 'iveness', 'fulness', 'ousness', 'aliti', 'ivitti', 'biliti', 'anci', 'eli']
        to_suffix_consideration = ['ate', 'tion', 'ence', 'ize', 'able', 'al', 'ent', 'ous',
                                   'ize', 'ate', 'ate', 'al', 'ive', 'ful', 'ous', 'al', 'ive', 'ble', 'ance', 'e']

        '''
        USED IN STEP 3
        '''
        from_ication_suffix = ['icate', 'ative',
                               'alize', 'iciti', 'ical', 'ful', 'ness']
        to_ication_suffix = ['ic', '', 'al', 'ic', 'ic', '', '']

        '''
        USED IN STEP 4
        '''
        from_one_plus_suffix_consider = ['al', 'ance', 'ence', 'er', 'ic', 'able', 'ible',
                                         'ant', 'ement', 'ment', 'ent', 'ion', 'ou', 'ism', 'ate', 'iti', 'ous', 'ive', 'ize']

        # 1st STEP SECTION

        '''
        Step 1A

        1. SESS -> SS
        2. IES -> I
        3. SS -> SS
        4. S -> Remove
        '''

        zipped_list = zip(from_str, to_str)

        for item in zipped_list:
            if input_str.endswith(item[0]):
                input_str = input_str[0: len(
                    input_str) - len(item[0])] + item[1]

        '''
        Step 1B

        1. (m > 0)EED -> EE
        2. *[V]ED -> *[V]
        3. *[V]ING -> *[V]
        '''
        if len(input_str) > 3:
            if input_str.endswith('eed'):
                input_str = input_str[0: len(input_str) - len('eed')] + 'ee'

            if input_str.endswith(('ed')) and input_str[-3] in vowel_list:
                input_str = input_str[0: len(input_str) - len('ed')] + ''

            if input_str.endswith(('ing')) and input_str[-3] in vowel_list:
                input_str = input_str[0: len(input_str) - len('ing')] + ''

        '''
        Step 1C

        1. *[V]Y -> *[V]i
        '''
        if len(input_str) > 2:
            if input_str.endswith('y') and input_str[-2] in vowel_list:
                input_str = input_str[0: len(input_str) - len('y')] + 'i'

        # 2nd STEP SECTION

        '''
        Step 2
        
        1. (m>0)ATIONAL -> ATE
        2. (m>0)TIONAL -> TION
        3. (m>0)ENCI -> ENCE
        4. (m>0)IZER -> IZE
        5. (m>0)ABLI -> ABLE
        6. (m>0)ALLI -> AL
        7. (m>0)ENTLI -> ENT
        8. (m>0)OUSLI -> OUS
        9. (m>0)IZATION -> IZE
        10. (m>0)ATION -> ATE
        11. (m>0)ATOR -> ATE
        12. (m>0)ALISM -> AL
        13. (m>0)IVENESS -> IVE
        14. (m>0)FULNESS -> FUL
        15. (m>0)OUSNESS -> OUS
        16. (m>0)ALITI -> AL
        17. (m>0)IVITI -> IVE
        18. (m>0)BILITI -> BLE
        19. (m>0)ANCI -> ANCE
        20. (m>0)ELI -> E
        '''

        zipped_suffix_list = zip(from_suffix_consideration,
                                 to_suffix_consideration)

        for suffix in zipped_suffix_list:
            if len(input_str) > len(suffix[0]) + 1:
                if input_str.endswith(suffix[0]):
                    input_str = input_str[0: len(
                        input_str) - len(suffix[0])] + suffix[1]

        # 3rd STEP SECTION

        '''
        Step 3

        1. (m>0)ICATE -> IC
        2. (m>0)ATIVE -> ''
        3. (m>0)ALIZE -> AL
        4. (m>0)ICITI -> IC
        5. (m>0)ICAL -> IC
        6. (m>0)FUL -> ''
        7. (m>0)NESS -> ''
        '''

        zipped_ication_suffix = zip(from_ication_suffix,
                                    to_ication_suffix)

        for suffix in zipped_ication_suffix:
            if len(input_str) > len(suffix[0]) + 1:
                if input_str.endswith(suffix[0]):
                    input_str = input_str[0: len(
                        input_str) - len(suffix[0])] + suffix[1]

        # 4th STEP SECTION

        '''
        Step 4

        1. (m>1)AL -> ''
        2. (m>1)ANCE -> ''
        3. (m>1)ENCE -> ''
        4. (m>1)ER -> ''
        5. (m>1)IC -> ''
        6. (m>1)ABLE -> ''
        7. (m>1)IBLE -> ''
        8. (m>1)ANT -> ''
        9. (m>1)EMENT -> ''
        10. (m>1)MENT -> ''
        11. (m>1)ENT -> ''
        12. ((m>1)and(*S or *Y))ION -> ''
        13. (m>1)OU -> ''
        14. (m>1)ISM -> ''
        15. (m>1)ATE -> ''
        16. (m>1)ITI -> ''
        17. (m>1)OUS -> ''
        18. (m>1)IVE -> ''
        19. (m>1)IZE -> ''
        '''

        # zipped_one_plus_suffix_consider = zip(from_one_plus_suffix_consider,
        #                             to_one_plus_suffix_consider)

        for suffix in from_one_plus_suffix_consider:
            if len(input_str) > len(suffix) + 1:

                if suffix == 'ion':
                    if (input_str[-4] == 'y' or input_str[-4] == 's') and len(input_str) > 4:
                        input_str = input_str[0: len(
                            input_str) - len(suffix)]
                        continue
                if input_str.endswith(suffix):
                    input_str = input_str[0: len(
                        input_str) - len(suffix)]

        return input_str


class Preprocessing():

    def __init__(self):
        '''
        Couple of steps in the below two lines
        Here, os.path.abspath('.') is
        '/home/saif/Downloads/University/Semester VI/Information Retrieval/Sir Zeeshan/Assignment/Findex/server/models'
        So, what I did was,

        1. Reverse the above string,
        2. Find the position of '/' that comes first
        3. Extract substr starting from that position all the way to the end
        4. Reverse back the string
        5. Append the `data/` folder path
        '''
        self.reversed_abspath = os.path.abspath('.')

        # Data folder path
        self.data_path = self.reversed_abspath + "/data"

        # Dist folder path
        self.dist_path = self.reversed_abspath + "/dist"

        # To store the retrieved file paths
        self.file_paths = []

        # stop word list
        self.stop_words_list = []

        # Total words
        self.total_words = []

        # PORTER STEMMER
        self.porter_stemmer = PorterStemmer()

        # NLTK - Regex Tokenizer, for removing punctuation
        self.nltk_tokenizer = nltk.RegexpTokenizer(r"\w+")

        # LEMMATIZATION
        nltk.download('wordnet')
        self.wordnet_lemmatizer = WordNetLemmatizer()

    # Get file paths
    def store_file_paths(self):
        for path in pathlib.Path(self.data_path).rglob('*.txt'):
            self.file_paths.append(str(path.parent) + "/" + str(path.name))

    # load the stop words/

    def load_stop_words(self):

        # Open the stop words file
        with open(f"{self.data_path}/Stopword-List.txt", mode='r') as file:

            # ... Going through the file until EOF - end of file
            for line in file:

                # Removing possible misc UTf-8 characters
                line = line.strip('\n')
                line = line.strip(' ')

                # Appending to the `stop_words` list
                self.stop_words_list.append(line)

    def pipeline(self, line,
                 porter_stemmer_to_stem, wordnet_lemmatizer_for_lemma):
        '''
        TOKENIZER

        This does the following steps described below. 

        Taking an example,
        "“Yes,” said Ivan Abramitch, looking pensively out of window, “it is
        never too late to marry."

        The following steps demonstrate what they do

        1. First removes punctuation, then tokenizes them, using nltk

        Yes said Ivan Abramitch looking pensively out of window it is 
        never too late to marry

        ['Yes', 'said', 'Ivan', 'Abramitch', 'looking', 'pensively', 'out', 
        'of', 'window', 'it', 'is', 'never', 'too', 'late', 'to', 'marry']

        2. Uses case folding - that is, just makes the tokens lower cased

        ['yes', 'said', 'ivan', 'abramitch', 'looking', 'pensively', 'out', 
        'of', 'window', 'it', 'is', 'never', 'too', 'late', 'to', 'marry']

        3. Finally, removing tokens

        ['yes', 'said', 'ivan', 'abramitch', 'looking', 'pensively', 'out', 
        'of', 'window', 'it', 'is', 'never', 'too', 'late', 'marry']
        '''
        tokens = AuxPreprocessing.Tokenizer(
            line, self.nltk_tokenizer, self.stop_words_list)

        '''
        PORTER STEMMER

        This turns our previous input into the following
        >>> ['ye', 'said', 'ivan', 'abramitch', 'look', 'pensiv', 'out', 'of', 
        'window', 'it', 'is', 'never', 'too', 'late', 'to', 'marri']
        '''
        tokens = AuxPreprocessing.Stemmer(tokens, porter_stemmer_to_stem)

        '''
        # LEMMATIZATION

        This turns our previous input into the following
        >>> ['ye', 'said', 'ivan', 'abramitch', 'look', 'pensiv', 'out', 'of', 
        'window', 'it', 'is', 'never', 'too', 'late', 'to', 'marri']
        '''
        tokens = AuxPreprocessing.Lemmatize_func(
            tokens, wordnet_lemmatizer_for_lemma)

        '''
        CHECK AGAIN FOR STOP WORDS

        Parse tokens list again if any punctuation result through
        stemmer and lemma
        '''
        for token in tokens:
            if token.strip(' ') in self.stop_words_list:
                tokens.remove(token)

        return tokens

    # preprocess data files

    def process_pipeline(self, file_path: str, total_word_list: list):

        with open(file_path, mode='r') as file:

            for line in file:

                # Simply extract the tokens
                tokens = self.pipeline(
                    line, self.porter_stemmer, self.wordnet_lemmatizer)

                # Append the tokens in a final list
                for token in tokens:
                    if token not in total_word_list and not token.isnumeric():
                        total_word_list.append(token)

    def save_total_words(self):
        '''
        If the path `../dist` does not exist, create it
        '''
        if not os.path.exists(self.dist_path):
            os.makedirs(self.dist_path)

        '''
        Store the list `total_words` at the location
        `../dist/Total-Words.txt`
        '''
        with open(f"{self.dist_path}/Total-Words.csv", mode='w') as file:
            for idx, word in enumerate(self.total_words):
                file.write(f"{idx},{word},\n")

    def data_load_and_save(self):
        '''
        Loads the file paths for all the files
        '''
        self.store_file_paths()

        '''
        Loads the stop words
        '''
        self.load_stop_words()

        '''
        Goes through each each from `store_file_path()` and processes it through,
        
        1. Document collection - all the data in one place
        2. Tokenization
            2.1. Removes punctuation
            2.2. Tokenizes each line
            2.3. Case folding, lower casing
            2.4. Stop word removal
        3. Stemmer
        4. Lemmatization 
        '''
        for file_path in self.file_paths:
            self.process_pipeline(file_path, self.total_words)

        '''
        Saves the total_words list as a TEXT file at the
        location `../dist/Total-Words.txt`
        '''
        self.save_total_words()


class IndexPreprocessing():

    def __init__(self):
        self.reversed_abspath = os.path.abspath('.')

        # Data folder path
        self.data_path = self.reversed_abspath + "/data"

        # Dist folder path
        self.dist_path = self.reversed_abspath + "/dist"

        # To store the retrieved file paths
        self.file_paths = []

        # stop word list
        self.stop_words_list = []

        # stop word list
        self.unique_word_counter = -500

        # NLTK - Regex Tokenizer, for removing punctuation
        self.nltk_tokenizer = nltk.RegexpTokenizer(r"\w+")

        # LEMMATIZATION
        self.wordnet_lemmatizer = WordNetLemmatizer()

        # Very annoying UTF 8 characters
        self.very_annoying_utf_8_characters = [
            '\n', '\r', '\"', '\'', '.', '’', ',', '“' '”', ';', '“', '!', '”', '”', '“', '-']

        # path_name_list
        self.path_name_list = []

        # Stemmer
        self.stemmer = PorterStemmer()        

        # patlib.Path results
        pathlib_walked_path = pathlib.Path(self.data_path).rglob('*.txt')

        # waste generation
        next(pathlib_walked_path)

        # path_name_parent
        path_name_parent, path_name_seen = '', False

        path_name_file_extension = next(pathlib_walked_path).name.split('.')[1]

        # Get the file paths for each of the short stories
        for path in pathlib_walked_path:

            if not path_name_seen:
                path_name_seen = True
                path_name_parent = path.parent

            self.path_name_list.append(int(str(path.name).split('.')[0]))

        self.path_name_list = [
            f"{str(entry)}.{path_name_file_extension}" for entry in sorted(self.path_name_list)]

        self.file_paths = [
            f"{str(path_name_parent)}/{str(path_name_entry)}" for path_name_entry in self.path_name_list]

    def process_data_through_pipelines(self):

        short_stories_path = f"{self.dist_path}/ShortStories"

        if not os.path.exists(short_stories_path):
            os.makedirs(short_stories_path)

        for path in self.file_paths:

            tokens = []

            with open(path) as file:

                # for line in file:
                data = file.readlines()

                for idx, _ in enumerate(data):
                    for remove_character in self.very_annoying_utf_8_characters:
                        data[idx] = data[idx].replace(remove_character, ' ')
                        data[idx] = re.sub(' +', ' ', data[idx].strip())

                data = ' '.join([entry for entry in data if entry !=
                                 '' and not entry.isnumeric()])
                tokens = [token.lower() for token in data.split(' ')]

                # STEMMING ->> LEMMATIZATION
                tokens = [self.wordnet_lemmatizer.lemmatize(
                    self.stemmer.stem(token)) for token in tokens]

                with open(f"{short_stories_path}/{path.split('/')[-1].split('.')[0]}.txt", mode='w') as file:
                    file.write(' '.join(tokens))

    def generate_positional_index(self, str_to_build_positional: str, positional_index: PositionalIndex):

        short_stories_path = []
        total_positions = ''
        for path in self.file_paths:
            short_stories_path.append(path.replace('data', 'dist'))

        for file_path_idx, path in enumerate(short_stories_path):

            positions = ''

            with open(path) as file:
                tokens = file.readlines()[0].split(' ')

                # TODO - I haven't tested how accurately this works
                for idx, token in enumerate(tokens):
                    if str_to_build_positional == token:
                        positions += f"{idx},"

            if positions != '':
                positions = f"{file_path_idx + 1},{positions[0:-1]};"
                total_positions = total_positions + positions

        positional_index.document_listing_positions = total_positions

    def for_line_store_file(self, line: str):

        # Preprocessing / cleaning
        entry = line.strip('\n').split(',')[0:2]

        # generate positional index
        positional_index = PositionalIndex(
            unique_hash=f"{entry[0]}")

        # Get the postiings from the parse
        self.generate_positional_index(entry[1], positional_index)

        content_dump = positional_index.__dict__

        if content_dump['document_listing_positions'] == ['']:
            return

        # opening file to save
        with open(f"{self.dist_path}/positional.txt", mode='a') as positional_file, open(f"{self.dist_path}/inverted.txt", 'a') as inverted_file:

            final_inverted_string = ''
            for line in content_dump['document_listing_positions'].split(';'):
                tokens = line.split(',')
                if line == '' or tokens == ['']:
                    continue
                final_inverted_string += f"{tokens[0]},{len(tokens)-1};"

            if final_inverted_string == '':
                return

            positional_file.write(
                f"{content_dump['unique_hash']}-{content_dump['document_listing_positions']}\n")
            inverted_file.write(
                f"{content_dump['unique_hash']}-{final_inverted_string}\n")

    def get_saved_normalized_words(self):

        total_words_list = []
        with open(f"{self.dist_path}/Total-Words.csv") as file:
            for line in file:
                total_words_list.append(line)

        with mp.Pool(10) as p:
            p.map(self.for_line_store_file, total_words_list)
