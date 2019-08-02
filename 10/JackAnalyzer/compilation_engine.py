import logging
logging.basicConfig(level=logging.DEBUG, filemode='w', filename='debug.log',
                    format='%(message)s')

class CompilationEngine:
    """ 
    Gets input in form of a list that has been parsed by tokenizer 
    """

    def __init__(self, input):

        self.output = ''
        self.input = input
        self.row = 0
        self.identation = ''
        self.TYPE = 'int', 'char', 'boolean'

        self.compile_class()

    def has_more_tokens(self):
        if self.input:
            return True
        return False


    def advance(self):
        self.token = self.input[0]
        self.input.pop(0)
        self.row += 1


    def compile_class(self):
        """ 'class' className '{' classVarDec* subroutineDec* '}' """

        self.output += '<class>\n'
        self.identation += '\t'
        self.output += self.wrap('keyword', 'class')

        self.advance()

        if self.next_is('identifier', check_type=True):
            self.output += self.wrap(self.token.tokentype, self.token.token)
        else:
            self.error('identifier')

        self.advance()

        if self.next_is('{'):
            self.output += self.wrap(self.token.tokentype, self.token.token)
        else:
            self.error('{')

        self.advance()

        self.compile_classVarDec()

        self.compile_subroutine()

        if self.token.token == '}':
            self.output += self.wrap(self.token.tokentype, self.token.token)
        else:
            self.error('}')

        self.output += '</class>\n'


    def compile_subroutine(self):
        """ Syntax: (constructor | function | method)
                    (void | type)  subroutineName '('
                    parameterList ')' subroutineBody
        """

        while not self.next_is('}'):

            self.open_ident('subroutineDec')

            if self.next_is('constructor', 'function', 'method'):
                self.output += self.wrap(self.token.tokentype, self.token.token)
            else:
                return

            self.advance()

            if self.next_is(self.TYPE):
                self.output += self.wrap(self.token.tokentype, self.token.token)
            else:
                self.error('void or type')

            self.advance()

            if self.next_is('identifier', check_type=True):
                self.output += self.wrap(self.token.tokentype, self.token.token)
            else:
                self.error('subroutineName')

            self.advance()

            if self.next_is('('):
                self.output += self.wrap(self.token.tokentype, self.token.token)
            else:
                self.error('(')

            self.advance()

            self.compile_parameterList()

            if self.next_is(')'):
                self.output += self.wrap(self.token.tokentype, self.token.token)
            else:
                self.error(')')

            self.advance()

            self.compile_subroutineBody()

            self.close_ident('subroutineDec')



    def compile_subroutineBody(self):
        """ Syntax: '{' varDec* statements '}' """
        
        self.open_ident('subroutineBody')

        if self.next_is('{'):
            self.output += self.wrap(self.token.tokentype, self.token.token)
        else:
            self.error('{')

        self.advance()

        self.compile_varDec()

        self.compile_statements()

        if self.next_is('}'):
            self.output += self.wrap(self.token.tokentype, self.token.token)
        else:
            self.error('}')

        self.close_ident('subroutineBody')


    def compile_statements(self):
        """ statement* 
            Syntax: letStatement | ifStatement | whileStatement | 
                    doStatement  | returnStatement
        """

        if not self.next_is('}'):
            self.open_ident('statements')

            while not self.next_is('}'):

                self.compile_do()
                self.compile_if()
                self.compile_let()
                self.compile_while()
                self.compile_return()

            self.close_ident('statements')            

        return


    def compile_do(self):
        """ Syntax: 'do' subroutineCall ';' """


    def compile_if(self):
        """ Syntax: 'if' '(' expression ')' '{' statements '}'
                     ('else' '{' statements '}')?
        """

    def compile_let(self):
        """ Syntax: 'let' varName ('[' expression ']')?
                    '=' expression ';'
        """

    def compile_while(self):
        """ Syntax: 'while' '(' expression ')'
                    '{' statements '}'
        """

    def compile_return(self):
        """ Syntax: 'return' expression? ';' """
    




    def compile_varDec(self):
        """ Syntax: 'var' type varName (',' varName)* ';' """

        while not self.next_is('let', 'if', 'while', 'do', 'return'):

            if self.next_is('var'):
                self.output += self.wrap(self.token.tokentype, self.token.token)
            else:
                self.error('var')

            self.advance()

            if self.next_is(self.TYPE):
                self.output += self.wrap(self.token.tokentype, self.token.token)
            else:
                self.error('type')
                
            self.advance()

            if self.next_is('identifier', check_type=True):
                self.output += self.wrap(self.token.tokentype, self.token.token)
            else:
                self.error('identifier')

            self.advance()

            self.check_more_varNames()

            if self.next_is(';'):
                self.output += self.wrap(self.token.tokentype, self.token.token)
            else:
                self.error(';')

        return



    def compile_parameterList(self):
        """ Syntax: ((type varName) (',' varName)*)? """

        if not self.next_is(')'):

            self.open_ident('parameterList')

            if self.next_is(self.TYPE):
                self.output += self.wrap(self.token.tokentype, self.token.token)
            else:
                self.error('type')

            self.advance()

            if self.next_is('identifier', check_type=True):
                self.output += self.wrap(self.token.tokentype, self.token.token)
            else:
                self.error('varName')

            self.advance()

            while not self.next_is(')'):
                
                if self.next_is(','):
                    self.output += self.wrap(self.token.tokentype, self.token.token)
                else:
                    self.error(',')

                self.advance()

                if self.next_is(self.TYPE):
                    self.output += self.wrap(self.token.tokentype, self.token.token)
                else:
                    self.error('type')

                self.advance()

                if self.next_is('identifier', check_type=True):
                    self.output += self.wrap(self.token.tokentype, self.token.token)
                else:
                    self.error('type')

                self.advance()

            self.close_ident('parameterList')

        else:
            return


    def compile_classVarDec(self):
        """ ('static' | 'field') type varName (',' varName)* '}' """

        while not self.next_is('constructor', 'function', 'method', '}'):
                    
            if self.next_is('field', 'static'):
                self.open_ident('classVarDec')
                self.output += self.wrap(self.token.tokentype, self.token)
            else:
                return
            
            self.advance()

            if self.next_is(self.TYPE):
                self.output += self.wrap(self.token.tokentype, self.token.token)
            else:
                self.error('type')

            self.advance()

            if self.next_is('identifier', check_type=True):
                self.output += self.wrap(self.token.tokentype, self.token.token)
            else:
                self.error('varName')

            self.advance()

            self.check_more_varNames()

            if self.next_is(';'):
                self.output += self.wrap(self.token.tokentype, self.token)

            self.close_ident('classVarDec')

            self.advance()

        return


    def open_ident(self, keyword):
        self.output += '<%s>' % keyword
        self.identation += '\t'

    def close_ident(self, keyword):
        self.output += '</%s>' % keyword
        self.identation -= '\t'



    def check_more_varNames(self):
        """ Syntax: ', varName' """

        while not self.next_is(';'):

            if self.next_is(','):
                self.output += self.wrap(self.token.tokentype, self.token.token)

            self.advance()
            
            if self.next_is('identifier', check_type=True):
                self.output += self.wrap(self.token.tokentype, self.token.token)
            else:
                self.error('varName')

            self.advance()

    
    def next_is(self, *args, check_type=False)
        """
        Checks if next token corresponds to expection.
        If kwargs are passed, the tokentype is checked instead
        of the token values itself
        """

        if check_type:
            return self.token.tokentype == *args

        for arg in args:
            # Special handling for type tokens
            if arg == self.TYPE:
                for _type in arg:
                    if (self.token.token == _type or 
                        self.token.tokentype == 'identifier'):
                        return True

            return self.token.token == arg

    def error(self, expected):
        raise NameError('Expected %s, at row: %s' % (expected, self.row))



    def wrap(self, identifier, token):
        return "{0}<{1}> {2} </{1}>\n".format(self.identation, identifier, token)




    def wrap_start(self, identifier, token):
        return "<{0}> {1} </{0}>\n\t".format(identifier, token)
            