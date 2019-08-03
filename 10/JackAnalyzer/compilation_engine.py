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

        self.open_ident('class')

        self.output += self.wrap('keyword', 'class')

        self.advance()

        self.add_next_token('identifier', check_type=True)

        self.advance()

        self.add_next_token('{')

        self.advance()

        self.compile_classVarDec()

        self.compile_subroutineDec()

        self.add_next_token('}')

        self.close_ident('class')


    def compile_subroutineCall(self):
        """ Syntax: subroutineName '(' expressionList ')'
            | (className | varName) '.' subroutineName '('
            expressionList ')'

        """



    def compile_subroutineDec(self):
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

            self.add_next_token('identifier', check_type=True)

            self.advance()

            self.add_next_token('(')

            self.advance()

            self.compile_parameterList()

            self.add_next_token(')')

            self.advance()

            self.compile_subroutineBody()

            self.close_ident('subroutineDec')



    def compile_subroutineBody(self):
        """ Syntax: '{' varDec* statements '}' """
        
        self.open_ident('subroutineBody')

        self.add_next_token('{')

        self.advance()

        self.compile_varDec()

        self.compile_statements()

        self.add_next_token('}')

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



    def compile_expression(self, open=False):
        """ Temporary method for debugging purposes """
        
        self.open_ident('expression')

        self.open_ident('term')

        self.output += self.wrap(self.token.tokentype, self.token.token)

        self.close_ident('term')

        self.close_ident('expression')




    def compile_do(self):
        """ Syntax: 'do' subroutineCall ';' """
        
        if self.next_is('do'):
            self.open_ident('doStatement')
            self.add_next_token('do')
            self.advance()
        else:
            return

        self.compile_subroutine()

        self.advance()

        self.add_next_token(';')

        self.close_ident('doStatement')




    def compile_if(self):
        """ Syntax: 'if' '(' expression ')' '{' statements '}'
                     ('else' '{' statements '}')?
        """

        if self.next_is('if'):
            self.open_ident('ifStatement')
            self.add_next_token('if')
            self.advance()
        else:
            return


        self.add_next_token('(')

        self.advance()

        self.compile_expression()

        self.advance()

        self.add_next_token(')')

        self.advance()

        self.add_next_token('{')

        self.advance()

        self.compile_statements()

        self.advance()

        self.add_next_token('}')

        self.advance()

        if self.next_is('else'):

            self.add_next_token('else')

            self.advance()

            self.add_next_token('{')

            self.advance()

            self.compile_statements()

            self.advance()

            self.add_next_token('}')

            self.advance()


        self.close_ident('ifStatement')



    def compile_let(self):
        """ Syntax: 'let' varName ('[' expression ']')?
                    '=' expression ';'
        """

        if self.next_is('let'):
            self.open_ident('letStatement')
            self.add_next_token('let')
            self.advance()
        else:
            return


        self.add_next_token('identifier', check_type=True):

        self.advance()

        if not self.next_is('='):

            self.add_next_token('[')

            self.advance()

            self.compile_expression()

            self.advance()

            self.add_next_token('}')
        
        self.add_next_token('=')

        self.advance()

        self.compile_expression()

        self.advance()

        self.add_next_token(';')

        self.close_ident('letStatement')


    def compile_while(self):
        """ Syntax: 'while' '(' expression ')'
                    '{' statements '}'
        """

        if self.next_is('while'):
            self.open_ident('whileStatement')
            self.add_next_token('while')
            self.advance()
        else:
            return

        self.add_next_token('(')

        self.self.advance()

        self.compile_expression()

        self.advance()

        self.add_next_token(')')

        self.advance()

        self.add_next_token('{')

        self.advance()

        self.compile_statements()

        self.advance()

        self.add_next_token('}')
        
        self.close_ident('whileStatement')


    def compile_return(self):
        """ Syntax: 'return' expression? ';' """
    
        if self.next_is('return'):
            self.open_ident('returnStatement')
            self.add_next_token('return')
            self.advance()
        else:
            return

        if not self.next_is(';'):
            self.compile_expression()
            self.advance()

        self.add_next_token(';')

        self.close_ident('returnStatement')



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

            self.add_next_token('identifier', check_type=True):

            self.advance()

            self.check_more_varNames()

            self.add_next_token(';')

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

            self.add_next_token('identifier', check_type=True):

            self.advance()

            while not self.next_is(')'):
                
                self.add_next_token(',')

                self.advance()

                if self.next_is(self.TYPE):
                    self.output += self.wrap(self.token.tokentype, self.token.token)
                else:
                    self.error('type')

                self.advance()

                self.add_next_token('identifier', check_type=True):

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

            self.add_next_token('identifier', check_type=True):

            self.advance()

            self.check_more_varNames()

            self.add_next_token(';')

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

            self.add_next_token(',')

            self.advance()
            
            self.add_next_token('identifier', check_type=True):

            self.advance()


    def add_next_token(self, expected, check_type=False):
        """
        Checks if the next token is what's expected and appends it
        to the output. If the token isn't what's expected, 
        an error is raised. 
        """

        if self.next_is(expected, check_type=check_type):
            self.output += self.wrap(self.token.tokentype, self.token.token)
        else:
            self.error(expected)

    
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
            