import re

text = """
// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/10/ExpressionLessSquare/Main.jack

/** Expressionless version of projects/10/Square/Main.jack. */

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


def find_matches(pattern, text):
    matches = pattern.finditer(text)
    for match in matches:
        print(dir(match))
        start, end = match.span()
        print(text[start:end])

pattern_standard_comment = re.compile("/\*\b")
pattern_api_comment = re.compile("/\*\*.*\*/")
pattern_slash_comment = re.compile("//")

find_matches(pattern_api_comment, text)

