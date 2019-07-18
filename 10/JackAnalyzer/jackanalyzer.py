import os

from jacktokenizer import JackTokenizer

class File:

    def __init__(self, name, path, content):
        self.name = name
        self.path = path
        self.content = content


    def __repr__(self):
        return self.name


class JackAnalyzer:

    def __init__(self, input):
        
        self.files = self.open_input(input)



    def create_tokenizer(self):
        tokenizer = JackTokenizer(self.files)
        return tokenizer


    def open_input(self, input):
        """
        Makes sure that the input file/dir exists, then opens
        it and creates an object of each file of given input.
        The objects are stored in a list, which is returned.
        """
        opened_files = []

        if os.path.exists(input):
            abspath = os.path.abspath(input)

                # Opens a directory input
            if os.path.isdir(input):
                for each_file in os.listdir(input):
                    name, ext = os.path.splitext(each_file)
                    if ext == ".jack":
                        name += ext
                        path = os.path.join(abspath, name)
                        with open(path) as f:
                            content = f.read()
                            path = path.replace(".jack", ".xml")
                            each_file = File(name, path, content)
                            opened_files.append(each_file)

                # Opens a single file input 
            else:
                name, ext = os.path.splitext(input)
                if ext == ".jack":
                    name += ext
                    with open(abspath) as f:
                        content = f.read()
                        path = abspath.replace(".jack", ".xml")
                        single_file = File(name, path, content)
                        opened_files.append(single_file)
        else:
            print("File or Directory doesn't exist.")
            quit()

        return opened_files



if __name__ == "__main__":

    jackanalyzer = JackAnalyzer("Main.jack")

    for _file in jackanalyzer.files:
        tokenizer = jackanalyzer.create_tokenizer()

        while tokenizer.has_more_tokens():
            tokenizer.advance()

