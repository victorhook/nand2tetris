class CompilationEngine:
    """ 
    Gets input in form of a list that has been parsed by tokenizer 
    """

    def __init__(self, input):

        self.output = ''
        self.input = input
        self.row = 0

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
        """ 'class' className '(' classVarDec* subroutineDec* ')' """

        self.output += '<class>\n\t'
        self.output += self.wrap('keyword', 'class')

        self.advance()

        if self.next_is('identifier', type=True):
            self.output += self.wrap(self.token.tokentype, self.token.token)
        else:
            self.error('identifier')

        self.advance()

        if self.next_is('{'):
            self.output += self.wrap(self.token.tokentype, self.token.token)
        else:
            self.error('{')

        self.advance()

        if self.next_is('field', 'static'):
            self.compile_classVarDec()
        elif self.next_is('constructor', 'function', 'method'):
            self.compile_subroutineDec()
        
        self.advance()

        if self.token.token == '}':
            self.output += self.wrap(self.token.tokentype, self.token.token)
        else:
            self.error('}')

        self.output += '</class>\n'


    def compile_classVarDec(self):
        """ ('static' | 'field') type varName (',' varName)* '}' """

        self.output += '<classVarDec>\n\t'
        self.output += self.wrap(self.token.tokentype, self.token.token)

        self.advance()

        if self.next_is('int', 'char', 'boolean'):
            self.output += self.wrap(self.token.tokentype, self.token.token)
        else:
            self.error('type')

        self.advance()

        self.compile_varName()



    
    def next_is(self, *args, **kwargs)
        """
        Checks if next token corresponds to expection.
        If kwargs are passed, the tokentype is checked instead
        of the token values itself
        """

        if kwargs:
            args = [list(kwargs.values)[0]]

        for arg in args:
            return self.token.token == arg

    def error(self, expected):
        raise NameError('Expected %s, at row: %s' % (expected, self.row))



    def wrap(self, identifier, token):
        return "<{0}> {1} </{0}>\n".format(identifier, token)




    def wrap_start(self, identifier, token):
        return "<{0}> {1} </{0}>\n\t".format(identifier, token)
            