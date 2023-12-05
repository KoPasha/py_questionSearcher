<h1>question extractor/searcher</h1>

<h2>1. question Searcher</h2>
question Searcher is searching in chosen list of json files of specific stucture intended for COK examination in educenter.ru
<h3>questionSearchedCommands.py</h3> - for using in command line mode. arguments in the command line is the key words to look for
<h3>questionSearcherUICbyScheme.py</h3> - the "main" interface version of the search
other .py files are modules needed for a execution of a programs above

The right way to start program in a default way is in commmand line:

**python .\queFind.py**

<h2>2. question extractor</h2>

<h3>questionExtractor.py</h3> - will extract questions and answers from html files in the current folder by putting it's data to json files of the same name as html file (adding .json at the end of each file name)
command line arguments is supposed to be a path where question data will be extractod from

The right way to start program in a default way is in commmand line:

**python .\questionExtractor.py**

ps:
to make an executable use:
pyinstaller --onefile questionExtractor.py
pyinstaller --onefile queFind.py

with a questionSearcherUICbyScheme.py you also have to put searcherMainWindow.ui file in the same folder

to start a queFind without console window:
pythonw .\queFind.py