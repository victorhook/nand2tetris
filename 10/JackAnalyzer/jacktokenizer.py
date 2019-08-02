import os
import re

from compilation_engine import CompilationEngine

keywords = [
    "class",
    "constructor",
    "function",
    "method",
    "field",
    "static",
    "var",
    "int",
    "char",
    "boolean",
    "void",
    "true",
    "false",
    "null",
    "this",
    "let",
    "do",
    "if",
    "else",
    "while",
    "return",
]

symbols = [
    "{",
    "}",
    "(",
    ")",
    "[",
    "]",
    ".",
    ",",
    ";",
    "+",
    "-",
    "*",
    "/",
    "&",
    "|",
    "<",
    ">",
    "=",
    "~",
]

regex_meta = [
    ".", "$", "^", "*", "+", "?", "{", 
    "}", "[", "]", "\\", "|", "(", ")"
]

class File:

    def __init__(self, name, path, content):
        self.name = name
        self.path = path
        self.content = content

    def __repr__(self):
        return self.name


class Token:

    def __init__(self, token=None, tokentype=None):
        self.token = token
        self.tokentype = tokentype

    def __repr__(self):
        return f"{self.tokentype}: {self.token}"


class TokenType:

    def __init__(self, tokentype, pattern):
        self.tokentype = tokentype
        self.pattern = pattern

    def __repr__(self):
        return self.tokentype



class JackAnalyzer:

    def __init__(self, input):
        
        self.files = self.open_input(input)

    def create_tokenizer(self, file):
        tokenizer = JackTokenizer(file)
        return tokenizer


    def save_xml(self, file, content):
        with open(file.path, "w") as f:
            f.write(content)
            print(f"Saving '{file.name}' on location: {file.path}")


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



    def xml_check(self, token, tokentype):
        """ Adjusts the output to match XML output """

        if tokentype == 'stringConstant':
            token = token.replace('"', '')

        elif tokentype == 'symbol':
            if token == '<':
                token = '&lt;'
            elif token == '>':
                token = '&gt;'
            elif token == '"':
                token = '&quot;'
            elif token == '&':
                token = '&amp;'

        return token, tokentype




class JackTokenizer:

    def __init__(self, file):
        self.token = Token()
        self.file = self.clean_text(file)
        self.make_re_patterns()


    def clean_text(self, file):
        """
        Removes all comments /** ... */, /* ... */ or // ...
        Then removes all white space, both using the re module
        """
        content = "".join(file.content)

        # Removes API comments
        while True:                
            try:
                start = re.search(r'\/\*{1,2}', content).start()
                end = re.search(r'\*\/', content).end()
                
                string = content[start:end]
                content = content.replace(string, "")

            except AttributeError:
                break

        content = re.sub(r'\/\*{1,2}[^\/\*]*\*\/', "", content)
        # Remove backslash comments
        content = re.sub('//.*', "", content)
        # Replaces all whitespace with a single whitespace,
        # this is useful to seperate tokens later.
        content = re.sub('\s+', " ", content)

        file.content = content

        return file


    def advance(self):
        """
        Gets the next token from the string and sets the attributes
        of the token object to corresponding token and tokentype
        """

        self.file.content = self.remove_whitespace(self.file.content)

        for pattern in self.patterns:
            match = re.search(pattern.pattern, self.file.content)
            if match and match.start() == 0:
                token = self.file.content[match.start():match.end()]
                
                self.token.token = token
                self.token.tokentype = pattern.tokentype

                if self.intConst_not_valid(token):
                    raise ValueError("Integer not valid %s" % token)

                self.remove_last_token(token)
                self.file.content = self.remove_whitespace(self.file.content)
                self.trim_string()

                return self.token
        
        

    def trim_string(self):
        """ Removes "" from token if it's a string constant """
        if self.token.tokentype == "stringConstant":
            self.token.token = self.token.token.replace('"', '')


    def remove_whitespace(self, content):
        """ Checks if first character is white space and removes it """
        if content[0] == " ":
            content = re.sub(r'\s+', '', content, count=1)
        return content


    def remove_last_token(self, token):
        """ Removes the newly chosen token """
        self.file.content = self.file.content.replace(token, "", 1)


    def make_re_patterns(self):
        """ Makes the patterns that will be used to match the tokens with re """

        self.pattern_kw = TokenType("keyword", "(" + "|".join(keywords) + r")\b")

        self.pattern_sym = TokenType("symbol", r"[*\/&|<>=~{}()\[\].,;+-]")

        self.pattern_int = TokenType("integerConstant",r"\d{1,5}")

        self.pattern_ident = TokenType("identifier",r"[a-zA-Z_][a-zA-Z0-9_]*")

        self.pattern_str = TokenType("stringConstant",r'"[^"|.]*"')

        self.patterns = [ self.pattern_kw, self.pattern_sym, self.pattern_int, 
                        self.pattern_str, self.pattern_ident ]

        

    def intConst_not_valid(self, integer):
        """ Method to ensure integer matched is in allowed range """
        if integer.isdigit():
            if int(integer) < 0 or int(integer) > 32767:
                return True
        return False


    def has_more_tokens(self):
        if self.file.content:
            return True
        return False



if __name__ == "__main__":
    jackanalyzer = JackAnalyzer("/home/victor/coding/nand2tetris/nand2tetris_REAL/projects/10/ArrayTest")

    for _file in jackanalyzer.files:
        tokenizer = jackanalyzer.create_tokenizer(_file)
        comp_eng = CompilationEngine()

        tokens = []

        while tokenizer.has_more_tokens():
            token = tokenizer.advance()
            token.token, token.tokentype = jackanalyzer.xml_check(token.token, token.tokentype)        
            tokens.append(token)

        compilation_engine = CompilationEngine(tokens)

        









        # text = "<tokens>\n"
        # text += '<{kw}> {tok} </{kw}>\n'.format(kw=tokentype, tok=token)
        # text += '</tokens>'
        # jackanalyzer.save_xml(_file, text)
