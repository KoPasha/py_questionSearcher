import sys
def read_json_datafiles():
    result = []

def read_dataset():
    return read_json_datafiles()

def search(search_string, data_for_search):
    pass

def main():
    if len(sys.argv) > 1:
        search_string = sys.argv[1]
    else:
        search_string = ''
        print("You have to put file name as an argument to this program, or it will be using what ever it wants ]:/)")
    data_for_search = read_json_datafiles()

if __name__ == '__main__':
    main()