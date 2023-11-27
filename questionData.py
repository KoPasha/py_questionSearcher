
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

class COK_question:
    id: str
    q_text: str
    prompt: str
    options: list
    correct_answer: answer
    def __init__(self,id,q_text ='',prompt ='',options ='',correct_answer =''):
        self.id = ' '.join(id.split())
        self.q_text = ' '.join(q_text.split())
        self.prompt = ' '.join(prompt.split())
        self.correct_answer = ' '.join(correct_answer.split())
        if isinstance(options, list):
            self.options = options
        else:
            self.options = []
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
        for cur_option in data.options:
            self.add_option(cur_option['id'],cur_option['text'])

