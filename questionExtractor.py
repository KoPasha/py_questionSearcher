import sys
import bs4
import os.path
import json
import questionData

def is_answer_label(tag):
    if tag.has_attr('data-region') and tag['data-region'] == 'answer-label':
        return True
    return False

def get_question_from_div(que_div):
    qid = que_div['id'].replace('question-','')
    qtext = que_div.find(class_='qtext').text
    qprompt = que_div.find(class_='prompt').text
    correct_answer = que_div.find(class_='rightanswer').text
    answers = list()
    #going down through every child div in an answer div
    #   within this child div there is 'answer-label'
    #               with the number assigned to this answer in the nested span tag with a class 'answernumber'
    #   and also the answer by itseft contained in the div located next to span tag mentioned above
    for answer_child in que_div.find(class_='answer').children:
        if isinstance(answer_child,bs4.Tag):
            cur_answer_number = ''
            cur_answer_text = ''
            cur_answer_number_node = answer_child.find(is_answer_label)
            if isinstance(cur_answer_number_node,bs4.Tag):
                for cur_tag_within_an_answer in cur_answer_number_node.children:
                    if isinstance(cur_tag_within_an_answer,bs4.Tag):
                        if cur_tag_within_an_answer.name == 'span':
                            cur_answer_number = cur_tag_within_an_answer.text
                        elif isinstance(cur_tag_within_an_answer.text,str):
                            cur_answer_text = cur_tag_within_an_answer.text
            answers.append(questionData.answer(cur_answer_number,cur_answer_text))
    result = questionData.COK_question(qid,qtext,qprompt,answers,correct_answer)
    if result.is_empty(): 
        return None
    return result

def read_qdata_from_text(html):
    soup = bs4.BeautifulSoup(html, "lxml")
    divs_for_workthrough = soup.find_all("div", class_="que")
    all_questions_in_file = list()
    for cur_que_div in divs_for_workthrough:
        que = get_question_from_div(cur_que_div)
        if que != None:
            all_questions_in_file.append(que.data_for_json())
        #print(cur_que.attrs)
    if len(all_questions_in_file) > 0:
        #save to json file right next to the file that was just read
        json_object = json.dumps(all_questions_in_file)
        #print(json_object)
        return json_object
    print("*END OF FILE**************************")
    return None

def read_qdata_from_file(file_full_name):
    
    if os.path.isfile(file_full_name):
        if file_full_name[-4:].lower() == "html" or file_full_name[-3:].lower() == "htm":
            print("file name: %s \n" % file_full_name)
            try:
                with open(file_full_name,"r",encoding="utf8") as f:
                    html = f.read()
                    questions = read_qdata_from_text(html)
                    #after reading questions&answers we have to write json file filled with it
                    #json file have to be right next to an input file
                    file_full_name_json = file_full_name + '.json'
                    with open(file_full_name_json, "w") as outfile:
                        outfile.write(questions)
            except Exception as e:
                print("File is unreadable")
                print(e)
                return
    elif os.path.isdir(file_full_name):
        print("Folder name: %s \n" % file_full_name)
        for cur_file in os.scandir(file_full_name):
            read_qdata_from_file(cur_file.path)
    else:
        print("file does not exist")
    
def get_default_file_name():
    if sys.platform == "linux" or sys.platform == "linux2":
        return "Тестирование по Главе 1_ просмотр попытки.html"
    elif sys.platform == "darwin":
        return "Тестирование по Главе 1_ просмотр попытки.html"
    elif sys.platform == "win32" or sys.platform == "win64":
        return "C:\\mydocs\\2023-09-08\\"
        #"C:\\mydocs\\2023-09-08\\NFA_certificate1\\theme1\\"
        #return "C:\\mydocs\\2023-09-08\\NFA_certificate1\\theme1\\Тестирование по Главе 1_ просмотр попытки.html"
    
def main():
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = get_default_file_name()
        print("You have to put file name as an argument to this program, or it will be using what ever it wants ]:/)")
    read_qdata_from_file(file_name)
    #read_qdata_from_file(get_default_file_name())

if __name__ == "__main__":
    main()


