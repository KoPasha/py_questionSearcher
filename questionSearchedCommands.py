#question search without interface (interface options must me in other modules)
import sys
import os
import os.path
import json
import questionData
import datetime

def load_json_data_to_COK_data_structure(json_data, COK_data, source):
    for cur_json in json_data:
        try:
            cur_COK = questionData.COK_question(source=source).data_from_json(cur_json)
            COK_data.append(cur_COK)
        except Exception as e:
            print(f'error while reading json file, so problem is within the file: {e}')

def read_json_datafiles(path, data_structure):
    if os.path.isfile(path):
        if path[-4:].lower() == 'json':
            try:
                #read data structure from path
                with open(path,'r') as f:
                    current_json = json.load(f)
                    load_json_data_to_COK_data_structure(current_json, data_structure, source=os.path.basename(path))
            except Exception as e:
                print(f'upper level error while reading json file, so problem with a file: {e}')
    elif os.path.isdir(path):
        for cur_file in os.scandir(path):
            if os.path.basename(cur_file.path)[0] != '.':
                read_json_datafiles(cur_file.path, data_structure)

def read_dataset():
    result = []
    path_to_search_in = os.getcwd()
    read_json_datafiles(path_to_search_in,result)
    return result

#search_index - dict with keys is a letters and values is a nested dict with next letters in the words that were indexed
#               when dict key is not a letter but a word 'questions', 
#                      it means that it's value contains list of indexes of questions (from dataset) which text contains this words
def find_question_by_word(cur_word, search_index, create_if_not_found = False, index_if_create = -1):
    search_index_current_nest = search_index
    for cur_letter in cur_word:
        if (cur_letter == '*') and (not create_if_not_found):#query isn't for creating data, so it is enough to identify query by 'not create' flag
            ##we go through all nested nodes-letters below and get all questions contained in them in one result
            return get_all_nested_question_numbers(search_index_current_nest)
        else:
            search_index_next_nest = search_index_current_nest.get(cur_letter)
            if search_index_next_nest == None:#if that letter before this moment was't in index, then we creat new one
                if create_if_not_found:
                    search_index_next_nest = dict()
                    search_index_current_nest[cur_letter] = search_index_next_nest
                else:
                    return None
            search_index_current_nest = search_index_next_nest
    #so here is the moment were we reached the bottom of the tree
    # and we axpect to find a LIST of indexes of question with this word
    return get_question_numbers_for_nest(search_index_current_nest,create_if_not_found,index_if_create)

def get_all_nested_question_numbers(nest):
    result = list()
    for node_key, node_value in nest.items():#gives keys of this dict, which in this case is letters/'questions'
        if node_key == 'questions':#then the value is a list of indexes of questions
            result.extend(node_value)
        else:#this is a letter and the value must be dictionary
            if len(node_value) > 0:
                result.extend(get_all_nested_question_numbers(node_value))
    return result

def get_question_numbers_for_nest(nest, create_if_not_found, index_if_create):
    que_list = nest.get('questions')
    if que_list == None:
        if create_if_not_found:
            que_list = [index_if_create]
            nest['questions'] = que_list
        else:
            return None
    else:
        if create_if_not_found:
            que_list.append(index_if_create)
    return que_list

def search(search_string, data_for_search, search_index):
    #for a fast search we have to make a nested dict with a key tree of words/letters in keys of this dict
    # the values will be the indexes of questions that contains this word
    search_string_adopted = questionData.get_string_adopted_for_search(search_string,is_query=True)
    results = list()
    questions_found = None
    #search with a nested tree
    for cur_word in search_string_adopted.split():
        questions_found_now = find_question_by_word(cur_word, search_index)
        if questions_found_now != None:
            if questions_found != None:
                questions_found = questions_found.intersection(questions_found_now)
            else:
                questions_found = set()
                questions_found.update(questions_found_now)
    if questions_found != None:#in case no found question for every word in a search
        for cur_question_index in questions_found:
            results.append(data_for_search[cur_question_index])
    return results

def build_search_index(data_to_search):
    search_index = {}
    for cur_question in data_to_search:
        cur_question_index = data_to_search.index(cur_question)
        for cur_word in cur_question.united_question_text_for_search.split():
            find_question_by_word(cur_word, search_index, create_if_not_found = True, index_if_create = cur_question_index)
            # search_index_current_nest = search_index
            # for cur_letter in cur_word:
            #     search_index_next_nest = search_index_current_nest.get(cur_letter)
            #     if search_index_next_nest == None:#if that letter before this moment was't in index, then we creat new one
            #         search_index_next_nest = dict()
            #         search_index_current_nest[cur_letter] = search_index_next_nest
            #     search_index_current_nest = search_index_next_nest
            # #so here is the moment were we reached the bottom of the tree
            # # and we axpect to find a LIST of indexes of question with this word
            # que_list = search_index_current_nest.get('questions')
            # if que_list ==None:
            #     que_list = [cur_question_index]
            #     search_index_current_nest['questions'] = que_list
            # else:
            #     que_list.append(cur_question_index)
    return search_index
            

def optimize_dataset(data_for_search):
    print(f'before optimization {len(data_for_search)} timestamp: {datetime.datetime.now()}')

    indexes_to_delete = set()
    indexes_and_id_s = {}
    for cur_data in data_for_search:
        if indexes_and_id_s.get(cur_data.id) == None:#only the first appearance of question id must stay in search data
            indexes_and_id_s[cur_data.id] = data_for_search.index(cur_data)
        else:
            indexes_to_delete.add(data_for_search.index(cur_data))
    for index_to_delete in sorted(indexes_to_delete,reverse=True):
        data_for_search.pop(index_to_delete)
    print(f'after 1st optimization {len(data_for_search)} timestamp: {datetime.datetime.now()}')
    indexes_to_delete = set()
    indexes_and_id_s = {}
    for cur_data in data_for_search:
        if indexes_and_id_s.get(cur_data.united_question_hash) == None:#only the first appearance of question id must stay in search data
            indexes_and_id_s[cur_data.united_question_hash] = data_for_search.index(cur_data)
        else:
            indexes_to_delete.add(data_for_search.index(cur_data))
    for index_to_delete in sorted(indexes_to_delete,reverse=True):
        data_for_search.pop(index_to_delete)
    print(f'after 2nd optimization {len(data_for_search)} (size: {sys.getsizeof(data_for_search)}) timestamp: {datetime.datetime.now()}')


def main():
    if len(sys.argv) > 1:
        search_string = ' '.join(sys.argv[1:])
    else:
        search_string = 'Федеральным законом «О рынке ценных бумаг» заключение гражданско-правовых сделок с эмиссионными ценными бумагами, влекущих переход прав собственности на ценные бумаги является'
        print("You have to put one or more words as an argument to this program, or it woundn't give the questions back ]:/)")
    data_to_search_in = read_dataset()
    optimize_dataset(data_to_search_in)
    search_index = build_search_index(data_to_search_in)
    print(f'Search index (size: {sys.getsizeof(search_index)}) was built at timestamp: {datetime.datetime.now()}')
    results = search(search_string,data_to_search_in,search_index)
    for result in results:
        print(f'question: {result} \n')

if __name__ == '__main__':
    main()