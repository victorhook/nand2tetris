import re

text = """
// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/10/ExpressionLessSquare/Main.jack
/*dsad sad as a dsa */
/** Expressionless version of pro
jects/10/Square/Main.jack. */

class Main {
    static boolean test;    // Added for testing -- there is no static keyword
                            // in the Square files.

    function void main() {
        var SquareGame game;
        let game = game;
        do game.run();
        do game.dispose();
        return;
    }

    function void test() {  // Added to test Jack syntax that is not use in
        var int i, j;       // the Square files.
        var String s;
        var Array a;
        if (i) {
            let s = i;
            let s = j;
            let a[i] = j;
        }
        else {              // There is no else keyword in the Square files.
            let i = i;
            let j = j;
            let i = i | j;
        }
        return;
    }
}
"""


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
    "-",
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
    "_",
]

test = """
class Main() {

    function void main() {
        do Output.printString('Hey dude!');
    }

}
"""

pattern_kw = "(" + ")|(".join(keywords) + ")"
pattern_sym = "(" + ")|(".join(symbols) + ")"
pattern_int = "\d{1,5}"     # Matches an int between 0-32767 (needs to call func check_int)!
pattern_ident = "^\D[\d\w_]*"   # Matches any sequence of letter, digit or _, not start with digit
# pattern_str


def check_int(integer):
    if int(integer) < 0 or int(integer) > 32767:
        return False
    return True


matches = re.compile(pattern_kw).finditer(text)



# - Integer = 0-32767
# - String - A sequence of unicode characters not 
#            including double quotes " or new line
# - Identifier - A sequence of letters, digits and underscore
#                NOT starting with a digit

""