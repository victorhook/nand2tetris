import os
import re

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



    def create_tokenizer(self, file):
        tokenizer = JackTokenizer(file)
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

class JackTokenizer:

    def __init__(self, file):
        self.file = self.clean_text(file)
        print(self.file.content)

    def clean_text(self, file):
        """
        Removes all comments /** ... */, /* ... */ or // ...
        Then removes all white space, both using the re module
        """
        text = "".join(file.content)

        pattern_api_or_standard_comment = re.compile(r"/\*{1,2}(.|\n)*\*/")
        pattern_slash_comment = re.compile("//.*")

        content = re.sub(pattern_slash_comment, "", text)
        content = re.sub(pattern_api_or_standard_comment, "", content)

        # This is the text with space included, for easier debugging
        file.debug_content = content    
        content = re.sub(r"[\t\n\s*]", "", content)
        
        file.content = content

        return file

    def has_more_tokens(self):
        if self.tokens:
            return True
        return False

    def advance(self):
        pass

    
    def token_type(self):
        """ 
        returns one of:
        KEYWORD, SYMBOL, IDENTIFIER, INT_CONST, STRING_CONST 
        """
        
        pass


    def keyword(self):
        """ 
        returns one of:
        CLASS, METHOD, FUNCTION, CONSTRUCTOR, INT, BOOLEAN, CHAR,
        VOID, VAR, STATIC, FIELD, LET, DO, IF ELSE, WHILE, RETURN,
        TRUE, FALSE, NULL, THIS
        """
        pass
    
    def symbol(self):
        pass

    def identifier(self):
        pass

    def int_val(self):
        pass
    
    def string_val(self):
        pass



if __name__ == "__main__":
    jackanalyzer = JackAnalyzer("Main.jack")

    for _file in jackanalyzer.files:
        tokenizer = jackanalyzer.create_tokenizer(_file)

        # while tokenizer.has_more_tokens():
        #     tokenizer.advance()