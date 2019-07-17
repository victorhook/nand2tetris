class JackTokenizer:

    def __init__(self, file):
        self.file = file

    
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
    tokenizer = JackTokenizer("x")