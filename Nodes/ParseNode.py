from Nodes.Node import Node
from antlr4 import *
from Parse.MySqlLexer import MySqlLexer
from Parse.MySqlParser import MySqlParser
import re

class ParseNode(Node):

    def __str__(self):
        return f"Node {self.type} ({self.parsable})"

    def find_parse_text(self, input, pos):
        self.parsable = input[pos+8:input.find("END-EXEC", pos)].strip()
        return input.find("END-EXEC", pos)+8

    def parse(self, lexer_base, parser_base):    
        input_stream = InputStream(input)
        lexer = lexer_base(input_stream)
        stream = CommonTokenStream(CaseChangingStream(lexer, True))
        parser = parser_base(stream)
        tree = parser.root()
        return tree