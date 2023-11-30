#data structure for question extractor/searcher
import hashlib

class answer:
    id: str
    text: str
    def __init__(self,answer_id ='',answer_text=''):
        self.id = ' '.join(answer_id.split())
        self.text = ' '.join(answer_text.split())
    def is_empty(self):
        if (not isinstance(self.text, str)) or (isinstance(self.text,str) and (not self.text)):
            return True
        return False
    def data_for_json(self):
        return {'id': self.id, 'text': self.text}
    def data_from_json(self,data):
        self.text = data['text']
        self.id = data['id']

#for this we need to filter strings: no "one-letter-words", only words and numbers 
#   words and numbers cannot be in the same word
#   any separations are transformed to blanks
def get_string_adopted_for_search(search_string,is_query = False):
    result_string = ''
    prev_char = ''
    for curr_char in search_string.lower():
        if curr_char.isdigit() != prev_char.isdigit():#all times when digits comes right next to letter, they must be separated by blank
            result_string = result_string + ' '
        if curr_char.isdigit() or curr_char.isalpha():
            result_string = result_string + curr_char
        elif (curr_char == '*') and is_query:#asterisk is a special char, and its always comes last in a word (only for query strings, data strings get asterisks as blanks)
            result_string = f'{result_string}{curr_char} '
        else:
            result_string = result_string + ' '
        prev_char = curr_char
    return ' '.join(result_string.split())#get rid of unnecessary blanks

class COK_question:
    id: str
    q_text: str
    prompt: str
    options: list
    correct_answer: answer
    united_question_text: str
    united_question_hash: str
    united_question_text_for_search: str
    united_question_text_for_print: str
    def __str__(self) -> str:
        return self.united_question_text
    def __init__(self,id = '',q_text ='',prompt ='',options ='',correct_answer =''):
        self.id = ' '.join(id.split())
        self.q_text = ' '.join(q_text.split())
        self.prompt = ' '.join(prompt.split())
        self.correct_answer = ' '.join(correct_answer.split())
        if isinstance(options, list):
            self.options = options
        else:
            self.options = []
    def update_united_question_text(self):
        answers_in_str = ''
        answers_in_str_for_print = ''
        separator = ''#all answer strings but first need to be on the next line
        for count, option in enumerate(sorted(self.options,key=lambda x:x.text),1):
            answers_in_str = f"{answers_in_str} {count} {option.text}"#f"{answers_in_str} {option.id} {option.text}"
            answers_in_str_for_print = f"{answers_in_str_for_print}{separator}{count}: {option.text}"
            separator = '\n'#all answer strings but first need to be on the next line
        text_for_result = f"{self.q_text} {self.prompt} {answers_in_str} {self.correct_answer}"
        self.united_question_text = ' '.join(text_for_result.split()) 
        self.united_question_text_for_search = get_string_adopted_for_search(self.united_question_text)
        #self.united_question_hash = hashlib.md5(self.united_question_text.encode("utf-8")).hexdigest()
        self.united_question_hash = hashlib.sha1(self.united_question_text_for_search.encode("utf-8")).hexdigest()
        self.united_question_text_for_print = f"{self.q_text}\n{self.prompt}\n{answers_in_str_for_print}\n\n{self.correct_answer}"
    def clear_options(self):
        self.options.clear()
    def add_option(self,answer_id,answer_text):
        self.options.append(answer(answer_id,answer_text))
    def set_correct_answer(self,correct_answer):
        self.correct_answer = correct_answer
    def is_empty(self):
        if (not isinstance(self.q_text,str)) or (isinstance(self.q_text,str) and (not self.q_text)):#if string is empty
            return True
        return False
    def data_for_json(self):
        return {'id': self.id, 
                'q_text': self.q_text,
                'prompt': self.prompt,
                'correct_answer': self.correct_answer,
                'options': [option.data_for_json() for option in self.options]
                }
    def data_from_json(self,data):
        self.id = data['id']
        self.q_text = data['q_text']
        self.prompt = data['prompt']
        self.correct_answer = data['correct_answer']
        #also options should be unreavealed from json list
        #self.options = [answer(x,y) for x,y in data.options]
        self.clear_options()
        for cur_option in data['options']:
            self.add_option(cur_option['id'],cur_option['text'])
        self.update_united_question_text()
        return self

